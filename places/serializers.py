from rest_framework import serializers
from .models import Place, SuggestedEdit

class PlaceSerializer(serializers.ModelSerializer):
    permits_info = serializers.CharField(required=False, allow_blank=True),
    
    class Meta:
        model=Place
        exclude = ["created_by"] 

class SuggestedEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=SuggestedEdit
        fields='__all__'