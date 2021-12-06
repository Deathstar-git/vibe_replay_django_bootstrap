from django.test import TestCase

from main.models import Artist


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
