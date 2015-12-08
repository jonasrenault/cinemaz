from django.utils.timezone import get_current_timezone
from datetime import datetime
from rest_framework_mongoengine import serializers as drfme_serializers
from rest_framework import serializers as drf_serializers
from cinemas.models import Cinema, CodeName, Showtime, Screening, Movie, Release, Statistics


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


class ScreeningSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Screening
        fields = ('date', 'code')

    def to_internal_value(self, data):
        date = data.get('d')
        times = data.get('t')

        # Perform the data validation.
        if not date:
            raise drf_serializers.ValidationError({
                'd': 'This field is required.'
            })

        if not times:
            raise drf_serializers.ValidationError({
                't': 'This field is required.'
            })

        validated_data = list()
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        for time in times:
            t = datetime.strptime(time.get('$'), '%H:%M')
            tz = get_current_timezone()
            dt = tz.localize(parsed_date.replace(hour=t.hour, minute=t.minute))
            validated_data.append({
                'date': dt,
                'code': time.get('code')
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return validated_data



class ShowtimeSerializer(CustomModelSerializer, drfme_serializers.DocumentSerializer):
    class Meta:
        model = Showtime
        fields = ('screen_format', 'version', 'release_week', 'preview', 'display', 'movie', 'theater', 'screenings')

    def to_internal_value(self, data):
        update_json_keys(data, Showtime.FIELD_NAMES)


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
        code = data.get('code')
        name = data.get('name')
        if not code:
            raise drf_serializers.ValidationError({
                'code': 'This field is required.'
            })
        if not name:
            raise drf_serializers.ValidationError({
                'name': 'This field is required.'
            })

        # Return the validated values.
        return {
            'code': int(code),
            'name': name
        }


class ReleaseSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    country = CodeNameSerializer()
    distributor = CodeNameSerializer()
    release_state = CodeNameSerializer()

    class Meta:
        model = Release
        fields = ('release_date', 'country', 'distributor', 'release_state')

    def to_internal_value(self, data):
        update_json_keys(data, Release.FIELD_NAMES)
        release_date = data.get('release_date')
        if not release_date:
            raise drf_serializers.ValidationError({
                'release_date': 'This field is required.'
            })



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

    class Meta:
        model = Movie
        fields = ('code', 'title', 'original_title', 'synopsis', 'synopsis_short', 'runtime', 'poster', 'release',
                  'nationality', 'genre', 'statistics', 'casting_short', 'trailer')

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
            valid &= embedded_field.is_valid(raise_exception=raise_exception)

        return valid



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
            valid &= embedded_field.is_valid(raise_exception=raise_exception)

        return valid