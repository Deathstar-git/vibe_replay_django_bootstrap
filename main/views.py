# from django.contrib.auth import authenticate, login
# from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, FormView
from werkzeug.exceptions import InternalServerError
# from django.views.decorators.cache import cache_page
from .forms import RegisterUserForm, LoginUserForm, CommentForm
from .models import Artist, Account, Genre
from .utils import *


def search(request):
    if request.is_ajax():
        q = request.GET.get('query')  # с помощью аякса вытаскиваем данные,которые ввели
    else:
        return  # ну если не аякс запрос значит нахуй иди
    try:
        songs = Song.objects.filter(name__icontains=q)  # ищем такой обьект где имя похоже на q
    except InternalServerError:  # если не нашлось пишем "Ищем" типа не баг а фича
        return render(request, 'main/test.html', {'answer': "Ищем.."})
    return render(request, 'main/test.html', {'answer': songs})  # если нашлось выгружаем результат


class SongMain(DataMixin, ListView):
    model = Song
    template_name = 'main/testmain.html'
    context_object_name = 'songs'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('pl_id', 1)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', pl_id=1)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Song.objects.filter(playlist__pk=1)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация', pl_id=pl_id)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        u = form.save(commit=False)
        u.save()
        Account.objects.create(user=u)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('login')


class MyAccount(DataMixin, ListView):
    model = User
    template_name = 'main/my.html'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Личный кабинет', pl_id=1)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.pk)


def add_to_my(request, song_id):
    user = User.objects.get(pk=request.user.pk)
    song = Song.objects.get(pk=song_id)
    user.account.my_music.add(song)
    return redirect(request.META['HTTP_REFERER'])


def add_to_my_artist(request, a_id):
    user = User.objects.get(pk=request.user.pk)
    artist = Artist.objects.get(pk=a_id)
    user.account.my_artists.add(artist)
    return redirect('artist', a_id=a_id)


def del_to_my_artist(request, a_id):
    user = User.objects.get(pk=request.user.pk)
    artist = Artist.objects.get(pk=a_id)
    user.account.my_artists.remove(artist)
    return redirect('artist', a_id=a_id)


class PlaylistView(DataMixin, ListView):
    model = Song
    template_name = 'main/playlist.html'
    context_object_name = 'songs'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('pl_id', self.kwargs['pl_id'])
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Плейлисты', pl_id=self.kwargs['pl_id'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Song.objects.filter(playlist__pk=self.kwargs['pl_id'])


def get_playlist_data(request):
    pl_id = 1
    if request.method == 'GET':
        if 'pl_id' in request.COOKIES:
            pl_id = request.COOKIES['pl_id']
    if request.is_ajax():
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
        singers = Artist.objects.filter(song__in=songs_id)
        for a in singers:
            artist_names.append(str(a.name))
        data = {'artists': artist_names, 'songs': song_names,
                'songs_urls': song_urls, 'cover_urls': cover_urls,
                'songs_id': songs_id}
        return JsonResponse(data)


def get_mymusic_data(request):
    user = User.objects.get(pk=request.user.pk)
    songs = user.account.my_music.all()
    print(songs)
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
    singers = Artist.objects.filter(song__in=songs_id)
    for a in singers:
        artist_names.append(str(a.name))
    data = {'artists': artist_names, 'songs': song_names,
            'songs_urls': song_urls, 'cover_urls': cover_urls,
            'songs_id': songs_id}
    return JsonResponse(data)


# # @cache_page(60*15)
# def playlist(request, pl_id):
#
#     songs = Song.objects.filter(playlist__pk=pl_id)
#     context = {
#         'songs': songs,
#         'title': 'Плейлисты',
#         'menu': menu,
#         'pl_id': pl_id,
#         # 'pl_id_player': pl_id_player
#     }
#
#     # if request.user.is_authenticated:
#     #     return redirect('main')
#     # user = authenticate(username=username, password=password)
#     # if user is not None:
#     #     if user.is_active:
#     #         login(request, user)
#     #         return redirect('main')
#     #     else:
#     #         # Return a 'disabled account' error message
#     #         ...
#     # else:
#     #     # Return an 'invalid login' error message.
#     #     ...
#     response = render(request, 'main/playlist.html', context=context)
#     # response.set_cookie('pl_id_player', pl_id_player)
#     return response

# class LoginUser(DataMixin, LoginView):
#     form_class = LoginUserForm
#     template_name = 'main/login.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         pl_id = 1
#         if self.request.method == 'GET':
#             if 'pl_id' in self.request.COOKIES:
#                 pl_id = self.request.COOKIES['pl_id']
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Авторизация', pl_id=pl_id)
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_success_url(self):
#         return reverse('main')


class LoginUser(DataMixin,  LoginView):
    form_class = LoginUserForm  # форма авторизации from .forms import LoginUserForm
    template_name = 'main/login.html'  # htmlка для отображения

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация', pl_id=pl_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse('main')  # на какую страничку перейти в случае успеха

    # def post(self, request, *args, **kwargs):
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     data = {'username': username, 'password': password}
    #
    #     return self.render_to_response(data)

    # def render_to_response(self, context, **response_kwargs):
    #     response = super().render_to_response(context, **response_kwargs)
    #     return response
    #
    # def render_to_response(self, context):
    #     if self.request.is_ajax():
    #         return JSONResponseMixin.render_to_response(self, context)
    #     else:
    #         return self.render_to_response(context)

# def about(request):
#     pl_id = 1
#     answers = [['Вопрос1', 'Ответ1'], ['Вопрос2', 'Ответ2']]
#     context = {
#         'title': 'О нас',
#         'menu': menu,
#         'answers': answers,
#         'pl_id': pl_id
#     }
#     return render(request, 'main/about.html', context=context)


class AboutView(DataMixin, ListView):
    model = Song
    template_name = 'main/about.html'
    context_object_name = 'songs'

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О нас', pl_id=pl_id)
        return dict(list(context.items()) + list(c_def.items()))


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Всё фигня,давай по новой</h1>')


# def artists(request):
#     pl_id = 1
#     context = {
#         'title': 'Исполнители',
#         'menu': menu,
#         'pl_id': pl_id
#     }
#     return render(request, 'main/artists.html', context=context)


class ArtistsView(DataMixin, ListView):
    model = Artist
    template_name = 'main/artists.html'
    context_object_name = 'artists'

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Исполнители', pl_id=pl_id)
        return dict(list(context.items()) + list(c_def.items()))


# def categories(request):
#     pl_id = 1
#     context = {
#         'title': 'Жанры',
#         'menu': menu,
#         'pl_id': pl_id
#     }
#     return render(request, 'main/categories.html', context=context)


class CategoriesView(DataMixin, ListView):
    model = Genre
    template_name = 'main/categories.html'
    context_object_name = 'genres'

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Жанры', pl_id=pl_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Genre.objects.all()


def logout_user(request):
    logout(request)
    return redirect('main')


def download_song(request, song_id):
    # try:
    #     price = get_object_or_404(PriceList, is_active=True)
    # except MultipleObjectsReturned:
    #     return HttpResponse('Вы выбрали более одного файла')
    price = Song.objects.get(pk=song_id)
    return redirect(price.link.url)

# def entry(request):
#     pl_id = 1
#     context = {
#         'title': 'Войти',
#         'menu': menu,
#         'pl_id': pl_id
#     }
#     return render(request, 'main/login.html', context=context)


class ArtistView(ArtistDataMixin, ListView):
    model = Artist
    template_name = 'main/artist.html'
    context_object_name = 'artist'

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(pl_id=pl_id, a_id=self.kwargs['a_id'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Artist.objects.get(pk=self.kwargs['a_id'])


# class CategoryView(DataMixin, ListView):
#     model = Genre
#     template_name = 'main/category.html'
#     context_object_name = 'genre'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         pl_id = 1
#         if self.request.method == 'GET':
#             if 'pl_id' in self.request.COOKIES:
#                 pl_id = self.request.COOKIES['pl_id']
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Жанры', pl_id=pl_id)
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_queryset(self):
#         return Genre.objects.get(pk=self.kwargs['g_id'])


class SongView(DataMixin, ListView, FormView):
    model = Song
    form_class = CommentForm
    template_name = 'main/song.html'
    context_object_name = 'song'

    def get_context_data(self, *, object_list=None, **kwargs):
        pl_id = 1
        if self.request.method == 'GET':
            if 'pl_id' in self.request.COOKIES:
                pl_id = self.request.COOKIES['pl_id']
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Песня', pl_id=pl_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Song.objects.get(pk=self.kwargs['s_id'])


def send_comment(request, s_id):
    if request.method == 'POST':
        f = CommentForm(request.POST)
        comment = f.save()
        comment.song = Song.objects.get(pk=s_id)
        comment.author = Account.objects.get(user__pk=request.user.pk)
        f.save()
    # user = User.objects.get(pk=request.user.pk)
    # song = Song.objects.get(pk=s_id)
    # comment_song = song.comments_songs.all()
    # print(comment_song)
    # text = ""
    return redirect('song', s_id=s_id)
