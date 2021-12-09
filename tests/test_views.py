from django.test import TestCase
from main.models import Song
from django.urls import reverse


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание 10 песен для проверки отображения
        number_of_songs = 10
        for song_num in range(number_of_songs):
            Song.objects.create(name='Кукла Колдуна %s' % song_num,
                                link='songs_files/2021/12/09/Король_и_Шут_-_Кукла_Колдуна.mp3',
                                icon='songs/1.jpg', )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'main/testmain.html')
