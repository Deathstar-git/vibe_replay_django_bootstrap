from django.test import TestCase
from django.core.files.images import get_image_dimensions
from main.models import Artist, Song


class ArtistModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Artist.objects.create(name='Rammstein', biography='Крутые мужики')

    def test_name_label(self):
        author = Artist.objects.get(id=1)
        field_label = author._meta.get_field('name').verbose_name
        # Проверка валидности поля verbose_name для имени артиста
        self.assertEquals(field_label, 'Имя артиста')

    def test_first_name_max_length(self):
        author = Artist.objects.get(id=1)
        # Проверка на максимальную длину имени артиста
        max_length = author._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        author = Artist.objects.get(id=1)
        # Проверка на то,что ссылка на артиста может быть не найдена.
        print(author.get_absolute_url())
        self.assertEquals(author.get_absolute_url(), '/artists/1/')


class SongModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name='Кукла Колдуна', link='songs_files/2021/12/09/Король_и_Шут_-_Кукла_Колдуна.mp3',
                            icon='songs/1.jpg',)

    def test_link_max_length(self):
        song = Song.objects.get(id=1)
        # Проверка на максимальную длину ссылки
        max_length = song._meta.get_field('link').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        song = Song.objects.get(id=1)
        # Проверка на то,что ссылка на артиста может быть не найдена.
        print(song.get_absolute_url())
        self.assertEquals(song.get_absolute_url(), '/playlist/1/')

    def test_save_method(self):
        song = Song.objects.get(id=1)
        song.save()
        img = song.icon.path
        print(img)
        w, h = get_image_dimensions(img)
        self.assertTrue(w <= 125 and h <= 125)
