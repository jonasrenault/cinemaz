from cinemas.models import Cinema, CodeName
from cinemas.serializers import CinemaSerializer


def save_or_update_cinema(json):

    serializer = CinemaSerializer(data=json)
    if serializer.is_valid():
        cinema = serializer.save()
    return cinema


def save_or_update_code_name(json):
    try:
        chain = CodeName.objects.get(code=json['code'])
    except CodeName.DoesNotExist:
        chain = CodeName()

    set_property_if_exists(chain, json, 'code')
    set_property_if_exists(chain, json, 'name', '$')
    chain.save()
    return chain


def set_property_if_exists(model, json, model_property, json_property=None):
    if not json_property:
        json_property = model_property
    try:
        setattr(model, model_property, json[json_property])
    except (AttributeError, KeyError):
        pass