from allocine.services import AllocineService
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from cinemas import utils
from rest_framework_mongoengine import generics
from cinemas.models import Cinema, Movie
from cinemas.serializers import CinemaSerializer, MovieSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'cinemas': reverse('cinema-list', request=request, format=format),
        'movies': reverse('movie-list', request=request, format=format),
    })


class CinemaList(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ImportMovie(APIView):
    """
    Send a query for a movie to Allocine and import result in DB.
    """
    def get(self, request):
        service = AllocineService()
        profile = request.query_params.get('profile', 'large')
        code = request.query_params.get('code', None)

        allocine_response = service.get_movie(code=code, profile=profile)

        response = Response(status=allocine_response.status_code)
        data = allocine_response.json()
        response.data = data
        if 'movie' in data:
            utils.save_or_update_movie(data['movie'])

        return response


class ImportCinema(APIView):
    """
    Send a query for cinemas to Allocine and import results in DB.
    :param zip:
    :param profile:
    :param code:
    :param location:
    :param count:
    :param page:
    """
    def get(self, request):
        service = AllocineService()
        zip = request.query_params.get('zip', None)
        profile = request.query_params.get('profile', 'large')
        code = request.query_params.get('code', None)
        location = request.query_params.get('location', None)
        count = request.query_params.get('count', None)
        page = request.query_params.get('page', None)

        allocine_response = service.get_theaters(zip=zip, profile=profile, code=code, location=location, count=count,
                                                 page=page)

        response = Response(status=allocine_response.status_code)
        data = allocine_response.json()
        response.data = data
        if 'feed' in data and 'theater' in data['feed']:
            for cinema in data['feed']['theater']:
                utils.save_or_update_cinema(cinema)

        return response
