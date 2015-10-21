from cinemas.models import Cinema, CodeName, Movie


def save_or_update_movie(json):
    try:
        movie = Movie.objects.get(code=json['code'])
    except Movie.DoesNotExist:
        movie = Movie()

    set_property_if_exists(movie, json, 'code')
    set_property_if_exists(movie, json, 'title')
    set_property_if_exists(movie, json, 'runtime')
    set_property_if_exists(movie, json['castingShort'], 'directors')
    set_property_if_exists(movie, json['castingShort'], 'actors')
    set_property_if_exists(movie, json['castingShort'], 'creators')
    set_property_if_exists(movie, json['statistics'], 'user_rating' 'userRating')
    set_property_if_exists(movie, json['statistics'], 'user_review_count' 'userReviewCount')
    set_property_if_exists(movie, json['statistics'], 'user_rating_count' 'userRatingCount')
    set_property_if_exists(movie, json['statistics'], 'press_rating' 'pressRating')
    set_property_if_exists(movie, json['statistics'], 'press_review_count' 'pressReviewCount')
    set_property_if_exists(movie, json['statistics'], 'editorial_rating_count' 'editorialRatingCount')

    movie.save()
    return movie


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
        chain = save_or_update_code_name(json['cinemaChain'])
        cinema.chain = chain

    if json['geoloc']:
        set_property_if_exists(cinema, json['geoloc'], 'lat')
        set_property_if_exists(cinema, json['geoloc'], 'long')

    cinema.save()
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