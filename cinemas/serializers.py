from rest_framework import serializers
from cinemas.models import Cinema, CinemaChain


class CinemaSerializer(serializers.ModelSerializer):
    chain = serializers.PrimaryKeyRelatedField(many=False, queryset=CinemaChain.objects.all())
    screen_count = serializers.IntegerField(allow_null=True)
    lat = serializers.FloatField(allow_null=True)
    long = serializers.FloatField(allow_null=True)

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'code', 'address', 'postal_code', 'city', 'area', 'subway', 'lat', 'long',
                  'screen_count', 'has_PRM_access', 'has_event', 'open_to_external_sales', 'chain')


class CinemaChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaChain
        fields = ('id', 'name', 'code')