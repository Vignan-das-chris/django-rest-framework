from re import S
from rest_framework import serializers
from climates.models import Climate


class ClimateSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=150)
    date = serializers.DateField()
    temperature = serializers.IntegerField()

    def create(self, validated_data):
        return Climate.objects.create(**validated_data)
