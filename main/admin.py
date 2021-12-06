from django.contrib import admin
from .models import *


class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'song_language')
    list_filter = ('id', 'name', 'release_date')


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']


admin.site.register(Account, AccountAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Album)
admin.site.register(Playlist)
admin.site.register(Artist)
admin.site.register(Languages)
admin.site.register(Genre)
