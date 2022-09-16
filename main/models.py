from django.db import models
from django.urls import reverse
from django.conf import settings
from PIL import Image


class Artist(models.Model):  # Исполнитель
    name = models.CharField(max_length=255, null=False, verbose_name='Имя артиста')  # Заголовок
    biography = models.TextField(null=True, blank=True, verbose_name='Описание')  # Краткое описание
    img = models.ImageField(null=True, verbose_name='Картинка артиста', upload_to='artists/')
    header_img = models.ImageField(null=True, verbose_name='Шапка артиста', upload_to='artists/headers/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist', kwargs={'a_id': self.pk})

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'


class Album(models.Model):  # Альбом
    artist = models.ManyToManyField(Artist, verbose_name='Артист')  # Какой артист исполняет
    title = models.CharField(max_length=100, verbose_name='Название')  # Название альбома
    cover = models.ImageField(null=True, verbose_name='Обложка альбома', upload_to='albums/')
    comment = models.TextField(null=True, blank=True, verbose_name='Описание')  # Краткое описание
    release_date = models.DateField(null=True, blank=True, verbose_name='Дата релиза')  # Когда вышел
    count_of_plays = models.IntegerField(default=0, verbose_name='Прослушивания')  # Кол-во прослушиваний

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.cover.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.cover.path)

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Playlist(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')  # Название плейлиста
    release_date = models.DateField(null=True, verbose_name='Дата публикации')  # Когда вышел
    cover = models.ImageField(null=True, verbose_name='Обложка плейлиста', upload_to='playlists/')
    comment = models.TextField(null=True, blank=True, verbose_name='Описание')  # Краткое описание
    count_of_plays = models.IntegerField(default=0, verbose_name='Прослушивания')  # Кол-во прослушиваний

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.cover.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.cover.path)

    def get_absolute_url(self):
        return reverse('playlist', kwargs={'pl_id': self.pk})

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'
        ordering = ['release_date', 'title']


class Languages(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')  # Название языка

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class Genre(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')  # Название жанра

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Song(models.Model):  # Песня
    artist = models.ManyToManyField(Artist, verbose_name='Артист')  # Какой артист исполняет
    name = models.CharField(max_length=255, verbose_name='Название')  # Название песни
    link = models.FileField(max_length=255, verbose_name='Ссылка', upload_to='songs_files/%Y/%m/%d/')
    icon = models.ImageField(null=True, verbose_name='Обложка песни', upload_to='songs/')
    category = models.ManyToManyField(Genre, verbose_name='Жанр')  # Категория
    song_language = models.ManyToManyField(Languages, verbose_name='Язык исполнения')  # Язык исполнения
    release_date = models.DateField(null=True, blank=True, verbose_name='Дата релиза')  # Когда вышла
    date_upload = models.DateField(auto_now_add=True, verbose_name="Дата загрузки на сайт")
    count_of_plays = models.IntegerField(default=0, blank=True, verbose_name='Прослушивания')  # Кол-во прослушиваний
    album = models.ManyToManyField(Album, verbose_name='Альбом')  # Из какого альбома
    playlist = models.ManyToManyField(Playlist,  verbose_name='Плейлист')  # Есть ли в плейлистах

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.icon.path)

        if img.height > 125 or img.width > 125:
            output_size = (125, 125)
            img.thumbnail(output_size)
            img.save(self.icon.path)

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'

    def get_absolute_url(self):
        return reverse('song', kwargs={'s_id': self.pk})


class Account(models.Model):  # Профиль
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    my_music = models.ManyToManyField(Song, verbose_name='Моя музыка')
    my_artists = models.ManyToManyField(Artist, verbose_name="Мои исполнители")
    photo = models.ImageField(null=True, blank=True,
                              verbose_name='Картинка пользователя', upload_to='profiles/%Y/%m/%d')

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name="Песня",
                             blank=True, null=True, related_name="comments_songs")
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Автор коммента",blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Текст коммента")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

