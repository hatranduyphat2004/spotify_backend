from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from api.models.Track import Track
from api.serializers.TrackSerializer import TrackSerializer

model = SentenceTransformer('all-MiniLM-L6-v2')


class RecommendTrackView(APIView):
    def post(self, request):
        text = request.data.get("text", "").strip()
        if not text:
            return Response({
                "success": False,
                "message": "Vui lòng nhập mô tả."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---- Phân biệt: Nếu chứa từ khóa kích hoạt mở bài ----
        trigger_keywords = ["mở bài", "bật nhạc",
                            "phát bài", "cho nghe", "mở nhạc", "nghe"]
        lowered_text = text.lower()

        for keyword in trigger_keywords:
            if keyword in lowered_text:
                # Giả sử tên bài nằm sau từ khóa, ví dụ: "mở bài nana" => lấy "nana"
                title_part = lowered_text.split(keyword, 1)[-1].strip()

                if not title_part:
                    return Response({
                        "success": False,
                        "message": "Không tìm thấy tên bài hát trong câu."
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Tìm bài hát theo tên
                track = Track.objects.filter(
                    title__icontains=title_part).first()
                if track:
                    serializer = TrackSerializer(track)
                    return Response({
                        "success": True,
                        "message": "Tìm theo tên bài hát",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)

                return Response({
                    "success": False,
                    "message": "Không tìm thấy bài hát có tên phù hợp."
                }, status=status.HTTP_404_NOT_FOUND)

        # ---- Không chứa keyword => dùng gợi ý theo mô tả ----
        tracks = Track.objects.exclude(
            description__isnull=True).exclude(description__exact="")
        if not tracks.exists():
            return Response({
                "success": False,
                "message": "Không có bài hát nào để gợi ý."
            }, status=status.HTTP_404_NOT_FOUND)

        descriptions = [track.description for track in tracks]
        vectors = model.encode(descriptions)
        user_vector = model.encode([text])

        sims = cosine_similarity(user_vector, vectors)[0]
        best_index = int(np.argmax(sims))
        best_track = tracks[best_index]

        serializer = TrackSerializer(best_track)
        return Response({
            "success": True,
            "message": "Gợi ý theo mô tả thành công",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
