import os
import json

from django.test import SimpleTestCase
from django.conf import settings

from cinemas.models import Cinema
from cinemas.serializers import CinemaSerializer


class MovieSerializerTestCase(SimpleTestCase):

    def setUp(self):
        json_fixture = os.path.join(settings.BASE_DIR, 'cinemas/fixtures/cinema_c0102.json')

        with open(json_fixture, 'r') as f:
            self.json = json.load(f)

    def tearDown(self):
        Cinema.objects.all().delete()

    def test_cinema_serializer_should_be_valid(self):
        """
        Cinema serializer should be valid
        :return:
        """
        serializer = CinemaSerializer(data=self.json)
        self.assertTrue(serializer.is_valid())

    def test_should_create_model_with_correct_values(self):
        serializer = CinemaSerializer(data=self.json)
        serializer.is_valid()
        serializer.save()

        cinema = Cinema.objects.get(code='C0102')
        self.assertIsNotNone(cinema)
        self.assertEqual(cinema.code, self.json['code'])
        self.assertEqual(cinema.name, self.json['name'])
        self.assertEqual(cinema.address, self.json['address'])
        self.assertEqual(cinema.city, self.json['city'])
        self.assertEqual(cinema.postal_code, self.json['postal_code'])
        self.assertEqual(cinema.area, self.json['area'])
        self.assertEqual(cinema.subway, self.json['subway'])
        self.assertEqual(cinema.screen_count, self.json['screen_count'])
        self.assertEqual(cinema.has_PRM_access, False)
        self.assertEqual(cinema.has_event, False)
        self.assertEqual(cinema.open_to_external_sales, self.json['open_to_external_sales'])
        self.assertEqual(cinema.chain.name, self.json['chain']['name'])
        self.assertEqual(cinema.chain.code, self.json['chain']['code'])
        self.assertEqual(cinema.picture.href, self.json['picture']['href'])
        self.assertEqual(cinema.picture.path, self.json['picture']['path'])

