from django.urls import path
from api.views.AuthView import AuthView
from api.views.UserView import UserView
from api.views.ArtistView import ArtistView
from api.views.AlbumView import AlbumView
from api.views.TrackView import TrackView
from api.views.FolderView import FolderView
from api.views.GenreView import GenreView
from api.views.PlaylistView import PlaylistView
from api.views.ConversationView import ConversationListView, ConversationCreateView, DeleteConversationView
from api.views.ConversationMemberView import AddConversationMemberView
from api.views.MessageView import ConversationMessageHistoryView, MarkMessageAsReadView, DeleteMessageView, SendMessageView
from api.views.TransactionView import TransactionView
from api.views.SubscriptionPlanView import SubscriptionPlanView
from api.views.TransactionByOrderCodeView import TransactionByOrderCodeView
from api.views.StreamView import stream_mp3
from api.views.StreamView import get_audio_url
from api.views.TopTrackView import TopTrackView
from api.views.SearchView import SearchView
from api.views.ArtistTrackView import ArtistTrackView, ArtistTrackByTrackView, ArtistTrackByArtistView
from api.views.ArtistAlbumView import ArtistAlbumView, ArtistAlbumByAlbumView, ArtistAlbumByArtistView
from api.views.PopularityView import IncreasePopularityView
from api.views.GeminiView import ChatWithGeminiAPI
from api.views.RecommendTrackView import RecommendTrackView
from api.views.LyricView import LyricView
from api.views.UploadLyricView import UploadLyricView
from api.views.GetLyricByTrackView import GetLyricByTrackView
from api.views.UserLikedTrackView import UserLikedTrackView


urlpatterns = [
    path("like-track/", UserLikedTrackView.as_view()),
    path('like-track/user/<int:pk>/',
         UserLikedTrackView.as_view()),  # pk là user_id
    path('like-track/<int:pk>/', UserLikedTrackView.as_view()),       # pk là bản ghi
    path('like-track/user/<int:user_id>/track/<int:track_id>/',
         UserLikedTrackView.as_view()),
    #
    path('lyrics/upload/<int:track_id>/',
         UploadLyricView.as_view()),
    path('lyrics/track/<int:track_id>/', GetLyricByTrackView.as_view()),
    #
    path('lyrics/', LyricView.as_view()),
    path('lyrics/<int:pk>/', LyricView.as_view()),
    #
    path('presigned-url/<str:filename>/', get_audio_url),
    # Stream track
    path('stream/<str:filename>/', stream_mp3, name='stream_mp3'),
    # Auth
    path('auth/<str:action>/', AuthView.as_view(), name='auth-action'),
    # Artist
    path('artists/', ArtistView.as_view(),
         name='artist_list'),  # GET (all), POST
    path('artists/<int:pk>/', ArtistView.as_view(),
         name='artist_detail'),  # GET (one), PUT, DELETE
    # User
    path('users/', UserView.as_view(), name='user_list'),  # GET (all), POST
    path('users/<int:pk>/', UserView.as_view(),
         name='user_detail'),  # GET (one), PUT, DELETE
    path('users/<int:pk>/suspend/', UserView.as_view(),
         name='user_suspend'),  # PUT (suspend user)
    path('users/<int:pk>/active/', UserView.as_view(),
         name='user_active'),  # PUT (active user)


    # Album
    path('albums/', AlbumView.as_view(), name='album_list'),  # GET (all), POST
    path('albums/<int:pk>/', AlbumView.as_view(),
         name='album_detail'),  # GET (one), PUT, DELETE
    # Track
    path('tracks/', TrackView.as_view(), name='track_list'),  # GET (all), POST
    path('tracks/<int:pk>/', TrackView.as_view(),
         name='track_detail'),  # GET (one), PUT, DELETE
    path('tracks/album/<int:album_id>/', TrackView.as_view(),
         name='track_by_album'),  # GET tracks by album



    # Folder
    path('folders/', FolderView.as_view(),
         name='folder_list'),  # GET (all), POST
    path('folders/<int:pk>/', FolderView.as_view(),
         name='folder_detail'),  # GET (one), PUT, DELETE
    # Genre
    path('genres/', GenreView.as_view(), name='genre_list'),  # GET (all), POST
    path('genres/<int:pk>/', GenreView.as_view(),
         name='genre_detail'),  # GET (one), PUT, DELETE

    # Playlist
    path('playlists/', PlaylistView.as_view()
         ),             # GET all / POST new
    path('playlists/<int:pk>/', PlaylistView.as_view()),



    # Conversation
    path('conversations/', ConversationListView.as_view(),
         name='conversation-list'),
    path('conversations/create/', ConversationCreateView.as_view(),
         name='conversation-create'),
    path('conversations/<int:conversation_id>/delete/',
         DeleteConversationView.as_view(), name='conversation-delete'),
    path('conversations/<int:conversation_id>/messages/',
         ConversationMessageHistoryView.as_view(), name='conversation-message-history'),

    # Message
    path('conversations/<int:conversation_id>/send-message/',
         SendMessageView.as_view(), name='send-message'),
    path('messages/<int:message_id>/read/',
         MarkMessageAsReadView.as_view(), name='message-mark-read'),
    path('messages/<int:message_id>/delete/',
         DeleteMessageView.as_view(), name='message-delete'),

    # Conversation Member
    path('conversations/<int:conversation_id>/add-member/',
         AddConversationMemberView.as_view(), name='add-conversation-member'),

    # Transaction
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>/', TransactionView.as_view()),
    path('plans/', SubscriptionPlanView.as_view()),
    path('plans/<int:pk>/', SubscriptionPlanView.as_view()),
    #     path('payment-callback/', PayOSWebhookView.as_view(), name='payos-callback'),
    path('transactions/by-order-code/<int:order_code>/',
         TransactionByOrderCodeView.as_view()),

    # Artist-Track
    path('artist-tracks/', ArtistTrackView.as_view(), name='artist-track-list'),
    path('artist-tracks/<int:pk>/', ArtistTrackView.as_view(),
         name='artist-track-detail'),
    path('artist-tracks/track/<int:track_id>/',
         ArtistTrackByTrackView.as_view(), name='artist-track-by-track'),
    path('artist-tracks/artist/<int:artist_id>/',
         ArtistTrackByArtistView.as_view(), name='artist-track-by-artist'),


    # More Track
    path('tracks/recommended/', TopTrackView.as_view(),
         name='track_recommended'),  # GET (all), POST
    path('tracks/top', TopTrackView.as_view(), name='top_tracks'),

    # Artist-Album
    path('artist-albums/', ArtistAlbumView.as_view(), name='artist-album-list'),
    path('artist-albums/<int:pk>/', ArtistAlbumView.as_view(),
         name='artist-album-detail'),
    path('artist-albums/album/<int:album_id>/',
         ArtistAlbumByAlbumView.as_view(), name='artist-album-by-album'),
    path('artist-albums/artist/<int:artist_id>/',
         ArtistAlbumByArtistView.as_view(), name='artist-album-by-artist'),

    # Popularity
    path('tracks/<int:track_id>/increase-popularity/',
         IncreasePopularityView.as_view(), name='increase-popularity'),


    path('search/', SearchView.as_view(), name='search-track'),


    path("recommend-track/", RecommendTrackView.as_view(), name="recommend-track"),

    path('gemini/chat/', ChatWithGeminiAPI.as_view()),

]
