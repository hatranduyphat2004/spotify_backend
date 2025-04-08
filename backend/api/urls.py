from django.urls import path
from api.views.AuthView import AuthView
from api.views.UserView import UserView
from api.views.ArtistView import ArtistView
from api.views.AlbumView import AlbumView
from api.views.TrackView import TrackView

from api.views.ConversationView import ConversationListView, ConversationCreateView, DeleteConversationView
from api.views.ConversationMemberView import AddConversationMemberView
from api.views.MessageView import ConversationMessageHistoryView, MarkMessageAsReadView, DeleteMessageView, SendMessageView

urlpatterns = [
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
    # Album
    path('albums/', AlbumView.as_view(), name='album_list'),  # GET (all), POST
    path('albums/<int:pk>/', AlbumView.as_view(),
         name='album_detail'),  # GET (one), PUT, DELETE
    # Track
    path('tracks/', TrackView.as_view(), name='album_list'),  # GET (all), POST
    path('tracks/<int:pk>/', TrackView.as_view(),
         name='album_detail'),  # GET (one), PUT, DELETE
    
    # Conversation
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/create/', ConversationCreateView.as_view(), name='conversation-create'),
    path('conversations/<int:conversation_id>/delete/', DeleteConversationView.as_view(), name='conversation-delete'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessageHistoryView.as_view(), name='conversation-message-history'),
    
    # Message
    path('conversations/<int:conversation_id>/send-message/', SendMessageView.as_view(), name='send-message'),
    path('messages/<int:message_id>/read/', MarkMessageAsReadView.as_view(), name='message-mark-read'),
    path('messages/<int:message_id>/delete/', DeleteMessageView.as_view(), name='message-delete'),
    
    # Conversation Member
    path('conversations/<int:conversation_id>/add-member/', AddConversationMemberView.as_view(), name='add-conversation-member'),
    
]


