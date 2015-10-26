from cinemas.serializers import CinemaSerializer, ShowtimeSerializer, MovieSerializer
from cinemas.models import Cinema, Movie


def save_or_update_cinema(json):
    try:
        cinema = Cinema.objects.get(code=json['code'])
        serializer = Cinema(cinema, data=json)
    except Cinema.DoesNotExist:
        serializer = CinemaSerializer(data=json)

    if serializer.is_valid():
        cinema = serializer.save()
    return cinema


def save_showtime(json):
    cinema = Cinema.objects.get(code=json['place']['theater']['code'])
    if not cinema:
        raise Cinema.DoesNotExist('Unable to find cinema for showtime.')

    for showtime in json.get('movieShowtimes'):
        movie_json = showtime['onShow']['movie']
        save_or_update_movie(movie_json)


def save_or_update_movie(json):
    try:
        movie = Movie.objects.get(code=json['code'])
        serializer = MovieSerializer(movie, data=json)
    except Movie.DoesNotExist:
        serializer = MovieSerializer(data=json)

    if serializer.is_valid():
        movie = serializer.save()
    else:
        print('Oups, serializer is not valid')
        print(serializer.errors)

    return movie