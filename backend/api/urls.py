from django.urls import path
from api.views.AuthView import AuthView
from api.views.UserView import UserView
from api.views.ArtistView import ArtistView
from api.views.AlbumView import AlbumView

urlpatterns = [
   #Auth
    path('auth/<str:action>/', AuthView.as_view(), name='auth-action'),
   # Artist
    path('artists/', ArtistView.as_view(), name='artist_list'),  # GET (all), POST
    path('artists/<int:pk>/', ArtistView.as_view(), name='artist_detail'),  # GET (one), PUT, DELETE
   # User
    path('users/', UserView.as_view(), name='user_list'),  # GET (all), POST
    path('users/<int:pk>/', UserView.as_view(), name='user_detail'),  # GET (one), PUT, DELETE
    # Album
    path('albums/', AlbumView.as_view(), name='album_list'),  # GET (all), POST
    path('albums/<int:pk>/', AlbumView.as_view(), name='album_detail'),  # GET (one), PUT, DELETE
]
