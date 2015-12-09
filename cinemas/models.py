from mongoengine import *
import datetime


class CodeName(EmbeddedDocument):
    FIELD_NAMES = {
        '$': 'name',
    }
    name = StringField()
    code = IntField()


class Artwork(EmbeddedDocument):
    href = StringField()
    path = StringField()
    name = StringField()


class Statistics(EmbeddedDocument):
    FIELD_NAMES = {
        'userRatingCount': 'user_rating_count',
        'userReviewCount': 'user_review_count',
        'userRating': 'user_rating',
        'pressReviewCount': 'press_review_count',
        'pressRating': 'press_rating',
        'editorialRatingCount': 'editorial_rating_count',
    }
    user_rating_count = IntField(default=0)
    user_review_count = IntField(default=0)
    user_rating = FloatField()
    press_review_count = IntField(default=0)
    press_rating = FloatField()
    editorial_rating_count = IntField(default=0)


class CastingShort(EmbeddedDocument):
    directors = StringField(max_length=200)
    actors = StringField(max_length=200)
    creators = StringField(max_length=200)


class Release(EmbeddedDocument):
    FIELD_NAMES = {
        'releaseDate': 'release_date',
        'releaseState': 'release_state',
    }
    release_date = StringField(required=True, max_length=200)
    country = EmbeddedDocumentField(CodeName)
    distributor = EmbeddedDocumentField(CodeName)
    release_state = EmbeddedDocumentField(CodeName)


class Trailer(EmbeddedDocument):
    name = StringField(max_length=200)
    code = IntField(required=True)
    href = StringField(max_length=500)


class Version(EmbeddedDocument):
    FIELD_NAMES = {
        '$': 'name',
    }
    code = IntField(required=True)
    original = BooleanField(required=True)
    name = StringField(max_length=200)
    lang = IntField()


class Movie(Document):
    FIELD_NAMES = {
        'originalTitle': 'original_title',
        'synopsisShort': 'synopsis_short',
        'castingShort': 'casting_short',
        'productionYear': 'production_year'
    }
    code = IntField(required=True, unique=True)
    title = StringField(required=True, max_length=500)
    original_title = StringField(max_length=1000)
    synopsis = StringField()
    synopsis_short = StringField()
    runtime = IntField()
    poster = EmbeddedDocumentField(Artwork)
    release = EmbeddedDocumentField(Release)
    nationality = ListField(EmbeddedDocumentField(CodeName))
    genre = ListField(EmbeddedDocumentField(CodeName))
    statistics = EmbeddedDocumentField(Statistics)
    casting_short = EmbeddedDocumentField(CastingShort)
    trailer = EmbeddedDocumentField(Trailer)
    tag = ListField(EmbeddedDocumentField(CodeName))
    production_year = IntField()


class Cinema(Document):
    FIELD_NAMES = {
        'cinemaChain': 'chain',
        'postalCode': 'postal_code',
        'hasPRMAccess': 'has_prm_access',
        'openToExternalSales': 'open_to_external_sales',
        'hasEvent': 'has_event',
        'screenCount': 'screen_count',
    }

    name = StringField(required=True)
    code = StringField(required=True, unique=True)
    chain = EmbeddedDocumentField(CodeName)

    address = StringField()
    city = StringField()
    postal_code = StringField(max_length=50)
    area = StringField(max_length=200)
    subway = StringField(max_length=500)

    picture = EmbeddedDocumentField(Artwork)
    geoloc = PointField()

    screen_count = IntField()
    has_PRM_access = BooleanField(default=False)
    has_event = BooleanField(default=False)
    open_to_external_sales = BooleanField(default=False)
    updated_at = DateTimeField(default=datetime.datetime.now)


class Showtime(Document):
    FIELD_NAMES = {
        'screenFormat': 'screen_format',
        'releaseWeek': 'release_week',
        'scr': 'screenings',
    }
    screen_format = EmbeddedDocumentField(CodeName, required=True)
    version = EmbeddedDocumentField(Version, required=True)
    release_week = BooleanField(default=False)
    preview = BooleanField(default=False)
    movie = ReferenceField(Movie, required=True)
    theater = ReferenceField(Cinema, required=True)
    date = DateTimeField(required=True)
    code = IntField()
    ads = IntField()
    ticket = StringField(max_length=2000)
    seat_count = IntField()
    screen = EmbeddedDocumentField(CodeName)

