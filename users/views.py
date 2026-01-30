from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import RegisterSerializer
from .models import Customer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

# Registerview runs when the frontend sends a POST request (signup form).
class Registerview(APIView):
    def post(self, request):
        data=request.data
        serializers=RegisterSerializer(data=data)
        if serializers.is_valid():
            user=serializers.save()
            return Response({
                'message':'User created successfully!',
                'status':True,
                'data':serializers.data
            },status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class Loginview(APIView):
    def post(self,request):
        print('------->>request.data= ',request.data)
        data=request.data
        username = request.data.get('username')
        password = request.data.get('password')
        user = Customer.objects.filter(username=username).first()
        print('------>',user)
        if user:
            refresh=RefreshToken.for_user(user)
            return Response({
                'access_token':str(refresh.access_token),
                'refresh_token':str(refresh)
            })
        return Response({'message':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)

class Profileview(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user=request.user
        serializer=RegisterSerializer(user)
        return Response(serializer.data)
    