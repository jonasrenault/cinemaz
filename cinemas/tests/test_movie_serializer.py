import os
import json

from django.test import SimpleTestCase
from django.conf import settings

from cinemas.models import Movie
from cinemas.serializers import MovieSerializer


class MovieSerializerTestCase(SimpleTestCase):

    def setUp(self):
        json_fixture = os.path.join(settings.BASE_DIR, 'cinemas/fixtures/movie_14757.json')

        with open(json_fixture, 'r') as f:
            self.json = json.load(f)

    def tearDown(self):
        Movie.objects.all().delete()

    def test_movie_serializer_should_be_valid(self):
        """
        Movie serializer should be valid
        :return:
        """
        serializer = MovieSerializer(data=self.json)
        self.assertTrue(serializer.is_valid())

    def test_should_create_model_with_correct_values(self):
        serializer = MovieSerializer(data=self.json)
        serializer.is_valid()
        serializer.save()

        movie = Movie.objects.get(code='14757')
        self.assertIsNotNone(movie)
        self.assertEqual(movie.code, self.json['code'])
        self.assertEqual(movie.title, self.json['title'])
        self.assertEqual(movie.original_title, self.json['original_title'])
        self.assertEqual(movie.synopsis, self.json['synopsis'])
        self.assertEqual(movie.synopsis_short, self.json['synopsis_short'])
        self.assertEqual(movie.runtime, self.json['runtime'])
        self.assertEqual(movie.nationality[0].name, self.json['nationality'][0]['name'])
        self.assertEqual(movie.nationality[0].code, self.json['nationality'][0]['code'])

        self.assertEqual(movie.release.release_date, self.json['release']['release_date'])
        #self.assertEqual(movie.release.release_state.name, self.json['release']['release_state']['name'])

        self.assertEqual(movie.statistics.editorial_rating_count, self.json['statistics']['editorial_rating_count'])
        self.assertEqual(movie.statistics.user_rating, self.json['statistics']['user_rating'])
        self.assertEqual(movie.statistics.user_rating_count, self.json['statistics']['user_rating_count'])
        self.assertEqual(movie.statistics.user_review_count, self.json['statistics']['user_review_count'])

        self.assertEqual(movie.casting_short.actors, self.json['casting_short']['actors'])
        self.assertEqual(movie.casting_short.directors, self.json['casting_short']['directors'])


