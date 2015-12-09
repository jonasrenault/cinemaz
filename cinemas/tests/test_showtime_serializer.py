import os
import json

from django.test import SimpleTestCase
from django.conf import settings

from cinemas.models import Showtime, Cinema
from cinemas.serializers import TheaterShowtimeSerializer


class ShowtimeSerializer(SimpleTestCase):

    def setUp(self):
        json_fixture = os.path.join(settings.BASE_DIR, 'cinemas/fixtures/theater_showtime.json')

        with open(json_fixture, 'r') as f:
            self.json = json.load(f)

    def tearDown(self):
        Showtime.objects.all().delete()

    def test_serializer_should_create_showtime(self):
        """
        Serializer.save() should create showtime
        :return:
        """
        serializer = TheaterShowtimeSerializer(data=self.json)
        showtime = serializer.save()

        self.assertIsInstance(showtime, Showtime)

    def test_showtime_should_have_theater(self):
        serializer = TheaterShowtimeSerializer(data=self.json)
        showtime = serializer.save()

        cinema = Cinema.objects.get(code=self.json['place']['theater']['code'])
        self.assertEqual(showtime.theater, cinema)

