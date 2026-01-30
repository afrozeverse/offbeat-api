from rest_framework import serializers
from .models import Place, SuggestedEdit

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields='__all__'

class SuggestedEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=SuggestedEdit
        fields='__all__'