from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from allocine.services import AllocineService
from cinemas import utils
import simplejson as json
from rest_framework import viewsets
from cinemas.models import Cinema, CinemaChain
from cinemas.serializers import CinemaSerializer, CinemaChainSerializer
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
        return HttpResponse(json.dumps(data), content_type="application/json")

    return Http404("The request to the allocine api failed: " + response)


class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaChainViewSet(viewsets.ModelViewSet):
    queryset = CinemaChain.objects.all()
    serializer_class = CinemaChainSerializer