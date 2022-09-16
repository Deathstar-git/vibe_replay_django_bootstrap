from django.core.handlers.wsgi import WSGIRequest

from main.models import Song

menu = [
        {'title': "О проекте", 'url_name': 'about'},
        {'title': "Жанры", 'url_name': 'categories'},
        {'title': "Исполнители", 'url_name': 'artists'},
        {'title': "Мой Vibe", 'url_name': 'my'}]


class DataMixin:
    request: WSGIRequest

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu[-1] = {'title': "Войти", 'url_name': 'login'}
        context['menu'] = user_menu
        return context


class ArtistDataMixin:
    request: WSGIRequest

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        context['songs'] = Song.objects.filter(artist__pk=kwargs['a_id'])
        if not self.request.user.is_authenticated:
            user_menu[-1] = {'title': "Войти", 'url_name': 'login'}
        context['menu'] = user_menu
        return context
