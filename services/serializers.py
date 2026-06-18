from rest_framework import serializers
from .models import Service
 
class ServiceSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(read_only=True)  # set by view
 
    class Meta:
        model = Service
        fields = '__all__'
 