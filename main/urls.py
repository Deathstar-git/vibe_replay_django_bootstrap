from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('',  SongMain.as_view(), name='main'),
    path('playlist/<int:pl_id>/', PlaylistView.as_view(), name='playlist'),
    path('about', AboutView.as_view(), name='about'),
    path('artist/<int:a_id>/', ArtistView.as_view(), name='artist'),
    path('song/<int:s_id>/', SongView.as_view(), name='song'),
    path('send_comment/<int:s_id>/', views.send_comment, name='send_comment'),
    path('artists/', ArtistsView.as_view(), name='artists'),
    path('login', LoginUser.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('my', MyAccount.as_view(), name='my'),
    path('add_to_my/<int:song_id>/', views.add_to_my, name='add_to_my'),
    path('add_to_my_artist/<int:a_id>/', views.add_to_my_artist, name='add_to_my_artist'),
    path('del_to_my_artist/<int:a_id>/', views.del_to_my_artist, name='del_to_my_artist'),
    path('logout', views.logout_user, name='logout'),
    path('categories', CategoriesView.as_view(), name='categories'),
    # path('category/<int:g_id>/', CategoryView.as_view(), name='category'),
    path('download/<int:song_id>/', views.download_song, name='download'),
    path('search/', views.search, name='search'),
    path('get_mymusic_data', views.get_mymusic_data, name='get_mymusic_data'),
    path('get_playlist_data', views.get_playlist_data, name='get_playlist_data'),
]
