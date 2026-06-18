from rest_framework import serializers
from places.models import Place
from services.models import Service
from reviews.models import Review

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields='__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Service
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'