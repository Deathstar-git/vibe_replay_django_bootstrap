from django import template
from main.models import *
register = template.Library()


@register.inclusion_tag('main/list_playlists.html')
def show_playlists(curr_id=1):
    pl = Playlist.objects.all()
    return {'pl': pl, 'curr_id': curr_id}


@register.simple_tag()
def get_songs_info(pl_id):
    songs = Song.objects.filter(playlist__pk=pl_id)
    artist_names = []
    song_names = []
    song_urls = []
    cover_urls = []
    songs_id = []
    for s in songs:
        song_names.append(str(s.name))
        song_urls.append("/media/" + str(s.link))
        cover_urls.append("/media/" + str(s.icon))
        songs_id.append(str(s.pk))
    artists = Artist.objects.filter(song__in=songs_id)
    for a in artists:
        artist_names.append(str(a.name))
    return {'artists': artist_names, 'songs': song_names,
            'songs_urls': song_urls, 'cover_urls': cover_urls,
            'songs_id': songs_id}


@register.simple_tag()
def get_artist_by_song_name(song_id):
    song = Song.objects.get(pk=song_id)
    artist = list(Artist.objects.filter(song__pk=song.pk).values())
    return artist[0]['name']


@register.simple_tag()
def get_artist_link(song_id):
    song = Song.objects.get(pk=song_id)
    artist = Artist.objects.get(song__pk=song.pk)
    artist.get_absolute_url()
    return artist.get_absolute_url()
