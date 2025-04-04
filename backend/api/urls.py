from django.urls import path
from api.views import (
    RegisterView,
    LoginView,
    UserView,
    ArtistView,
    AlbumView,
    PlaylistView,
    MessageView,
    ConversationView,
    GenreView,
    FolderView,
    UserLikedTrackView,
    UserLikedAlbumView,
    UserFollowingArtistView,
    TrackView,
)

urlpatterns = [
    # Authentication
    path('api/auth/register/', RegisterView.as_view(), name='register'), #Đăng ký tài khoản
    path('api/auth/login/', LoginView.as_view(), name='login'), #Đăng nhập tài khoản

    # User Management
    path('users/', UserView.as_view(), name='user_list'),  # GET (all), POST
    path('users/<int:pk>/', UserView.as_view(), name='user_detail'),  # GET (one), PUT, DELETE

    # Artists
    path('artists/', ArtistView.as_view(), name='artist_list'),  # GET (all), POST
    path('artists/<int:pk>/', ArtistView.as_view(), name='artist_detail'),  # GET (one), PUT, DELETE

    # Albums
    path('albums/', AlbumView.as_view(), name='album_list'),  # GET (all), POST
    path('albums/<int:pk>/', AlbumView.as_view(), name='album_detail'),  # GET (one), PUT, DELETE

    # Playlists
    path('playlists/', PlaylistView.as_view(), name='playlist_list'),  # GET (all), POST
    path('playlists/<int:pk>/', PlaylistView.as_view(), name='playlist_detail'),  # GET (one), PUT, DELETE

    # Messages
    path('messages/', MessageView.as_view(), name='message_list'),  # GET (all), POST
    path('messages/<int:pk>/', MessageView.as_view(), name='message_detail'),  # GET (one), PUT, DELETE

    # Conversations
    path('conversations/', ConversationView.as_view(), name='conversation_list'),  # GET (all), POST
    path('conversations/<int:pk>/', ConversationView.as_view(), name='conversation_detail'),  # GET (one), PUT, DELETE

    # Genres
    path('genres/', GenreView.as_view(), name='genre_list'),  # GET (all), POST
    path('genres/<int:pk>/', GenreView.as_view(), name='genre_detail'),  # GET (one), PUT, DELETE

    # Folders
    path('folders/', FolderView.as_view(), name='folder_list'),  # GET (all), POST
    path('folders/<int:pk>/', FolderView.as_view(), name='folder_detail'),  # GET (one), PUT, DELETE

    # User Liked Tracks
    path('user-liked-tracks/', UserLikedTrackView.as_view(), name='user_liked_track_list'),  # GET (all), POST
    path('user-liked-tracks/<int:pk>/', UserLikedTrackView.as_view(), name='user_liked_track_detail'),  # GET (one), DELETE

    # User Liked Albums
    path('user-liked-albums/', UserLikedAlbumView.as_view(), name='user_liked_album_list'),  # GET (all), POST
    path('user-liked-albums/<int:pk>/', UserLikedAlbumView.as_view(), name='user_liked_album_detail'),  # GET (one), DELETE

    # User Following Artists
    path('user-following-artists/', UserFollowingArtistView.as_view(), name='user_following_artist_list'),  # GET (all), POST
    path('user-following-artists/<int:pk>/', UserFollowingArtistView.as_view(), name='user_following_artist_detail'),  # GET (one), DELETE

    # Tracks
    path('tracks/', TrackView.as_view(), name='track_list'),  # GET (all), POST
    path('tracks/<int:pk>/', TrackView.as_view(), name='track_detail'),  # GET (one), PUT, DELETE
]
