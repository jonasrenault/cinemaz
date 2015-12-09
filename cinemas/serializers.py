from rest_framework_mongoengine import serializers as drfme_serializers
from rest_framework import serializers as drf_serializers
from cinemas.models import Cinema, CodeName, Movie, Release, Statistics, CastingShort, Trailer, \
    Artwork, Showtime


class CustomModelSerializer(drf_serializers.ModelSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


def update_json_keys(data, key_dictionnary):
    """
    Updates the names of the keys in the data dictionnary to the values in key_dictionnary
    :param data:
    :param key_dictionnary:
    :return:
    """
    if isinstance(data, dict):
        for key in data.keys():
            new_key = key_dictionnary.get(key)
            if new_key:
                data[new_key] = data[key]
                del data[key]


class CodeNameSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = CodeName
        fields = ('name', 'code')

    def to_internal_value(self, data):
        """
        Takes the unvalidated incoming data as input and returns the validated data that will be made available as
        serializer.validated_data. The return value will also be passed to the .create() or .update() methods if .save()
        is called on the serializer class.
        """
        update_json_keys(data, CodeName.FIELD_NAMES)
        return super(CodeNameSerializer, self).to_internal_value(data)


class ReleaseSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    country = CodeNameSerializer(required=False)
    distributor = CodeNameSerializer(required=False)
    release_state = CodeNameSerializer(required=False)

    class Meta:
        model = Release
        fields = ('release_date', 'country', 'distributor', 'release_state')
        depth = 2

    def to_internal_value(self, data):
        update_json_keys(data, Release.FIELD_NAMES)
        return super(ReleaseSerializer, self).to_internal_value(data)

    def is_valid(self, raise_exception=False):
        """
        Call super.is_valid() and then apply embedded document serializer's validations.
        """
        valid = super(drfme_serializers.DocumentSerializer, self).is_valid(raise_exception=raise_exception)

        for embedded_field in self.embedded_document_serializer_fields:
            embedded_field.initial_data = self.validated_data.pop(embedded_field.field_name, drf_serializers.empty)
            try:
                valid &= embedded_field.is_valid(raise_exception=raise_exception)
            except drf_serializers.SkipField:
                # SkipField is called when a non required field is absent
                pass

        return valid


class ArtworkSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Artwork
        fields = ('name', 'href', 'path')


class TrailerSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Trailer
        fields = ('name', 'href', 'code')


class CastingShortSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = CastingShort
        fields = ('actors', 'directors', 'creators')


class StatisticsSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Statistics
        fields = ('user_rating_count', 'user_review_count', 'user_rating', 'press_review_count', 'press_rating',
                  'editorial_rating_count')

    def to_internal_value(self, data):
        update_json_keys(data, Statistics.FIELD_NAMES)
        return super(StatisticsSerializer, self).to_internal_value(data)


class MovieSerializer(CustomModelSerializer, drfme_serializers.DocumentSerializer):
    nationality = CodeNameSerializer(many=True, required=False)
    genre = CodeNameSerializer(many=True, required=False)
    release = ReleaseSerializer(required=False)
    statistics = StatisticsSerializer(required=False)
    casting_short = CastingShortSerializer(required=False)
    tag = CodeNameSerializer(many=True, required=False)
    trailer = TrailerSerializer(required=False)
    poster = ArtworkSerializer(required=False)

    class Meta:
        model = Movie
        fields = ('code', 'title', 'original_title', 'synopsis', 'synopsis_short', 'runtime', 'nationality', 'genre',
                  'release', 'statistics', 'casting_short', 'tag', 'trailer', 'production_year', 'poster')
        depth = 3

    def to_internal_value(self, data):
        update_json_keys(data, Movie.FIELD_NAMES)
        return super(MovieSerializer, self).to_internal_value(data)

    def is_valid(self, raise_exception=False):
        """
        Call super.is_valid() and then apply embedded document serializer's validations.
        """
        valid = super(drfme_serializers.DocumentSerializer, self).is_valid(raise_exception=raise_exception)

        for embedded_field in self.embedded_document_serializer_fields:
            embedded_field.initial_data = self.validated_data.pop(embedded_field.field_name, drf_serializers.empty)
            try:
                valid_embedded = embedded_field.is_valid(raise_exception=raise_exception)
                valid &= valid_embedded
            except drf_serializers.SkipField:
                # SkipField is called when a non required field is absent
                embedded_field._validated_data = {}

        return valid

    def create(self, validated_data):
        nationalities = validated_data.pop('nationality')
        genres = validated_data.pop('genre')
        tags = validated_data.pop('tag') if 'tag' in validated_data else list()

        movie = super(MovieSerializer, self).create(validated_data)

        for nationality in nationalities:
            movie.nationality.append(CodeName(**nationality))

        for genre in genres:
            movie.genre.append(CodeName(**genre))

        for tag in tags:
            movie.tag.append(CodeName(**tag))

        movie.save()
        return movie

    def update(self, instance, validated_data):
        nationalities = validated_data.pop('nationality')
        genres = validated_data.pop('genre')
        tags = validated_data.pop('tag')

        updated_instance = super(MovieSerializer, self).update(instance, validated_data)

        for nationality in nationalities:
            updated_instance.nationalities.append(CodeName(**nationality))

        for genre in genres:
            updated_instance.genre.append(CodeName(**genre))

        for tag in tags:
            updated_instance.tag.append(CodeName(**tag))

        updated_instance.save()
        return updated_instance


class CinemaSerializer(CustomModelSerializer, drfme_serializers.DocumentSerializer):
    chain = CodeNameSerializer()

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'code', 'chain', 'address', 'city', 'postal_code', 'area', 'subway',
                  'picture', 'screen_count', 'has_PRM_access', 'has_event', 'open_to_external_sales')

    def to_internal_value(self, data):
        update_json_keys(data, Cinema.FIELD_NAMES)
        return super(CinemaSerializer, self).to_internal_value(data)

    def is_valid(self, raise_exception=False):
        """
        Call super.is_valid() and then apply embedded document serializer's validations.
        """
        valid = super(drfme_serializers.DocumentSerializer, self).is_valid(raise_exception=raise_exception)

        for embedded_field in self.embedded_document_serializer_fields:
            embedded_field.initial_data = self.validated_data.pop(embedded_field.field_name, drf_serializers.empty)
            try:
                valid &= embedded_field.is_valid(raise_exception=raise_exception)
            except drf_serializers.SkipField:
                # SkipField is called when a non required field is absent
                pass

        return valid


class TheaterShowtimeSerializer:

    def __init__(self, data):
        self.initial_data = data

    def save(self):

        showtime = Showtime()

        return showtime