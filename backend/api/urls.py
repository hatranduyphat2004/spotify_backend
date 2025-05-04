from django.urls import path

from api.views.AlbumView import AlbumView
from api.views.ArtistView import ArtistView
from api.views.AuthView import AuthView
from api.views.ConversationMemberView import AddConversationMemberView
from api.views.ConversationView import ConversationListView, ConversationCreateView, DeleteConversationView
from api.views.FolderView import FolderView
from api.views.GenreView import GenreView
from api.views.MessageView import ConversationMessageHistoryView, MarkMessageAsReadView, DeleteMessageView, \
    SendMessageView
from api.views.PlaylistAddTrackView import PlaylistAddTrackView
from api.views.PlaylistView import PlaylistView
from api.views.TrackView import TrackView
from api.views.UserView import UserView

urlpatterns = [
    # Auth
    path('auth/<str:action>/', AuthView.as_view(), name='auth-action'),

    # Artist
    path('artists/', ArtistView.as_view(),
         name='artist_list'),  # GET (all), POST
    path('artists/<int:pk>/', ArtistView.as_view(),
         name='artist_detail'),  # GET (one), PUT, DELETE
    path('artists/count/', ArtistView.as_view(), name='artist-count'),

    # User
    path('users/', UserView.as_view(), name='user_list'),  # GET (all), POST
    path('users/<int:pk>/', UserView.as_view(),
         name='user_detail'),  # GET (one), PUT, DELETE
    path('users/<str:pk>/', UserView.as_view()),  # count user

    # Album
    path('albums/', AlbumView.as_view(), name='album_list'),  # GET (all), POST
    path('albums/<int:pk>/', AlbumView.as_view(),
         name='album_detail'),  # GET (one), PUT, DELETE

    # Track
    path('tracks/', TrackView.as_view(), name='track_list'),  # GET (all), POST
    path('tracks/<int:pk>/', TrackView.as_view(),
         name='track_detail'),  # GET (one), PUT, DELETE
    path('tracks/count/', TrackView.as_view()),  # Get Total Songs
    path('listen/count/', TrackView.as_view(), name='total-listens'),

    # Folder
    path('folders/', FolderView.as_view(),
         name='folder_list'),  # GET (all), POST
    path('folders/<int:pk>/', FolderView.as_view(),
         name='folder_detail'),  # GET (one), PUT, DELETE

    # Playlist + Add Track
    path('playlists/', PlaylistView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', PlaylistView.as_view(), name='playlist-detail'),
    path('playlists/add-track/', PlaylistAddTrackView.as_view(), name='playlist-add-track'),
    path('playlists/<int:playlist_id>/tracks/<int:track_id>/delete/', PlaylistView.as_view(),
         name='delete-track-from-playlist'),
    path('playlists/<int:pk>/delete/', PlaylistView.as_view(), name='delete-playlist'),

    # Genre
    path('genres/', GenreView.as_view(), name='genre_list'),  # GET (all), POST
    path('genres/<int:pk>/', GenreView.as_view(),
         name='genre_detail'),  # GET (one), PUT, DELETE

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

]
