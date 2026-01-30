from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Place,SuggestedEdit
from .serializers import PlaceSerializer,SuggestedEditSerializer #for now I am not using the SuggestedEditSerializer to reduce complexity of the project
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# here place details are sent from Backend to Frontend
@api_view( ['GET'])
def get_place(request):
    place=Place.objects.all()
    serializer=PlaceSerializer(place,many=True)
    return Response(serializer.data)
    
# here place details are sent from Frontend to Backend
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_place(request):
    serializer=PlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Update the place
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_place(request, id):
    # 1. Find the place
    try:
        place = Place.objects.get(id=id)
    except Place.DoesNotExist:
        return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

    # 2. Check if the logged-in user is the creator
    if place.created_by != request.user:
        return Response({'error': 'You are not allowed to update this place'}, 
                        status=status.HTTP_403_FORBIDDEN)

    # 3. Update the place
    serializer = PlaceSerializer(place, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()   # created_by remains same automatically
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_place(request, id):
    # 1. Get the place
    try:
        place = Place.objects.get(id=id)
    except Place.DoesNotExist:
        return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

    # 2. Check if logged-in user is the creator
    if place.created_by != request.user:
        return Response({'error': 'You are not allowed to delete this place'},
                        status=status.HTTP_403_FORBIDDEN)

    # 3. Delete
    place.delete()
    return Response({'message': 'Place deleted successfully'}, status=status.HTTP_200_OK)
