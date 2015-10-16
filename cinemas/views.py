from django.http import HttpResponse
from allocine.services import AllocineService
from cinemas import utils
import simplejson as json
from rest_framework import viewsets
from cinemas.models import Cinema, CinemaChain
from cinemas.serializers import CinemaSerializer, CinemaChainSerializer


def import_cinemas(request):
    service = AllocineService()
    data = service.get_theaters(zip='75000')
    if data:
        for cinema in data['feed']['theater']:
            utils.save_or_update_cinema(cinema)

    return HttpResponse(json.dumps(data), content_type="application/json")


class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaChainViewSet(viewsets.ModelViewSet):
    queryset = CinemaChain.objects.all()
    serializer_class = CinemaChainSerializer