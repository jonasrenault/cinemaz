from cinemas.models import Cinema, CinemaChain


def save_or_update_cinema(json):
    try:
        cinema = Cinema.objects.get(code=json['code'])
    except Cinema.DoesNotExist:
        cinema = Cinema()

    set_property_if_exists(cinema, json, 'code')
    set_property_if_exists(cinema, json, 'name')
    set_property_if_exists(cinema, json, 'address')
    set_property_if_exists(cinema, json, 'postal_code', 'postalCode')
    set_property_if_exists(cinema, json, 'city')
    set_property_if_exists(cinema, json, 'area')
    set_property_if_exists(cinema, json, 'subway')
    set_property_if_exists(cinema, json, 'screen_count', 'screenCount')
    set_property_if_exists(cinema, json, 'has_event', 'hasEvent')
    set_property_if_exists(cinema, json, 'has_PRM_access', 'hasPRMAccess')
    set_property_if_exists(cinema, json, 'open_to_external_sales', 'openToExternalSales')

    if json['cinemaChain']:
        chain = save_or_update_cinema_chain(json['cinemaChain'])
        cinema.chain = chain

    if json['geoloc']:
        set_property_if_exists(cinema, json['geoloc'], 'lat')
        set_property_if_exists(cinema, json['geoloc'], 'long')

    cinema.save()


def save_or_update_cinema_chain(json):
    try:
        chain = CinemaChain.objects.get(code=json['code'])
    except CinemaChain.DoesNotExist:
        chain = CinemaChain()

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