from rest_framework.views import APIView
from rest_framework.response import Response
from allocine.services import AllocineService
import requests


class AllocineCinema(APIView):
    """
    Send a search query for cinemas
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
        if allocine_response.status_code == requests.codes.ok:
            data = allocine_response.json()
            response.data = data

        return response


class AllocineMovie(APIView):
    """
    Send a query to get information on a Movie

    """
    def get(self, request):
        service = AllocineService()
        profile = request.query_params.get('profile', 'large')
        code = request.query_params.get('code', None)

        allocine_response = service.get_movie(code=code, profile=profile)

        response = Response(status=allocine_response.status_code)
        if allocine_response.status_code == requests.codes.ok:
            data = allocine_response.json()
            response.data = data

        return response


class AllocineShowtime(APIView):
    """
    Send a query to search for showtimes

    """
    def get(self, request):
        service = AllocineService()
        zip = request.query_params.get('zip', None)
        theaters = request.query_params.get('profile', None)
        movie = request.query_params.get('movie', None)
        location = request.query_params.get('location', None)
        date = request.query_params.get('date', None)
        count = request.query_params.get('count', None)
        page = request.query_params.get('page', None)

        allocine_response = service.get_showtimes(zip=zip, theaters=theaters, location=location, movie=movie,
                                                  date=date, count=count, page=page)

        response = Response(status=allocine_response.status_code)
        if allocine_response.status_code == requests.codes.ok:
            data = allocine_response.json()
            response.data = data

        return response
