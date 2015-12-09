from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from allocine.services import AllocineService
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from cinemas import utils
import simplejson as json
from rest_framework_mongoengine import generics
from cinemas.models import Cinema, Movie
from cinemas.serializers import CinemaSerializer, MovieSerializer
import requests


@require_http_methods(["GET"])
def import_cinemas(request):
    service = AllocineService()
    response = service.get_theaters(zip='75000')

    if response.status_code == requests.codes.ok:
        data = response.json()
        for cinema in data['feed']['theater']:
            utils.save_or_update_cinema(cinema)
        return HttpResponse(json.dumps(data), content_type="application/json")

    return Http404("The request to the allocine api failed: " + response)


@require_http_methods(["GET"])
def get_show_times(request):
    service = AllocineService()
    response = service.get_showtimes(zip=request.GET.get('zip'),
                                     theaters=request.GET.get('theaters'),
                                     location=request.GET.get('location'),
                                     movie=request.GET.get('movie'),
                                     date=request.GET.get('date'))

    if response.status_code == requests.codes.ok:
        data = response.json()
        for theater_showtime in data['feed']['theaterShowtimes']:
            utils.save_showtime(theater_showtime)
        return HttpResponse(json.dumps(data), content_type="application/json")

    return Http404("The request to the allocine api failed: " + response)


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
