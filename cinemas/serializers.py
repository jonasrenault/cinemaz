from rest_framework import serializers
from cinemas.models import Cinema, CodeName


class CinemaSerializer(serializers.ModelSerializer):
    chain = serializers.PrimaryKeyRelatedField(many=False, queryset=CodeName.objects.all())
    screen_count = serializers.IntegerField(allow_null=True)
    lat = serializers.FloatField(allow_null=True)
    long = serializers.FloatField(allow_null=True)

    class Meta:
        model = Cinema
        fields = ('pk', 'name', 'code', 'address', 'postal_code', 'city', 'area', 'subway', 'lat', 'long',
                  'screen_count', 'has_PRM_access', 'has_event', 'open_to_external_sales', 'chain')


class CodeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeName
        fields = ('id', 'name', 'code')