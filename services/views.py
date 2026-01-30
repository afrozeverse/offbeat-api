from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from users.models import Provider

@api_view(['GET'])
def get_services(request,place_id):
    services=Service.objects.filter(place_id=place_id)
    serializer=ServiceSerializer(services,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service(request):
    if not Provider.objects.filter(user=request.user).exists():
        return Response(
            {"error": "Only providers can create services"},
            status=status.HTTP_403_FORBIDDEN
        )
    serializer=ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({"detail": "Only providers can create services"},serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_service(request,id):
    # check the service exists or not
    try:
        service=Service.objects.get(id=id)
    except Service.DoesNotExist:
        return Response({'detail':'requested service doesnot exist'},status=status.HTTP_404_NOT_FOUND)
    
    # checks the user is provider or not
    if not Provider.objects.filter(user=request.user).exists():
        return Response(
            {"error": "Only providers can create services"},
            status=status.HTTP_403_FORBIDDEN
        )
    provider=Provider.objects.get(user=request.user)

    # checks he provider is the owner of the requested service or not
    if service.provider != provider:
        return Response({"detail": "You can update only your own services"},status=status.HTTP_403_FORBIDDEN)
    

    serializer= ServiceSerializer(service,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_service(request,id):
    # check the service exists or not
    try:
        service=Service.objects.get(id=id)
    except Service.DoesNotExist:
        return Response({'detail':'requested service doesnot exist'},status=status.HTTP_404_NOT_FOUND)
    
    # checks the user is provider or not
    if not Provider.objects.filter(user=request.user).exists():
        return Response(
            {"error": "Only providers can delete services"},
            status=status.HTTP_403_FORBIDDEN
        )
    provider=Provider.objects.get(user=request.user)

    # checks he provider is the owner of the requested service or not
    if service.provider != provider:
        return Response({"detail": "You can delete only your own services"},status=status.HTTP_403_FORBIDDEN)
    
    service.delete()
    return Response({'message':'Service deleted successfully'},status=status.HTTP_204_NO_CONTENT)