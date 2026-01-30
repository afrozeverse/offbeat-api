from rest_framework import serializers
from .models import Customer

class RegisterSerializer(serializers.ModelSerializer):
    #we declared the password2,beccause User mdoel doesnot contain default.
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=Customer
        fields=['username','email','password','password2']

    #this is to verify the password and confirm password(passwrod2) are same
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password must match")
        return data
    def create(self, validated_data):
        user=Customer.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        )
        return user 