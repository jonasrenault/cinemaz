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
