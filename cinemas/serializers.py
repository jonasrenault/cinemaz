from rest_framework_mongoengine import serializers as drfme_serializers
from rest_framework import serializers as drf_serializers
from cinemas.models import Cinema, CodeName


class CustomModelSerializer(drf_serializers.ModelSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CodeNameSerializer(CustomModelSerializer, drfme_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = CodeName
        fields = ('name', 'code')

    def to_internal_value(self, data):
        if isinstance(data, dict):
            for key in data.keys():
                new_key = CodeName.FIELD_NAMES.get(key)
                if new_key:
                    data[new_key] = data[key]
                    del data[key]
        return super(CodeNameSerializer, self).to_internal_value(data)


class CinemaSerializer(CustomModelSerializer, drfme_serializers.DocumentSerializer):
    chain = CodeNameSerializer()

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'code', 'chain', 'address', 'city', 'postal_code', 'area', 'subway',
                  'picture', 'screen_count', 'has_PRM_access', 'has_event', 'open_to_external_sales')

    def to_internal_value(self, data):
        if isinstance(data, dict):
            for key in data.keys():
                new_key = Cinema.FIELD_NAMES.get(key)
                if new_key:
                    data[new_key] = data[key]
                    del data[key]
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