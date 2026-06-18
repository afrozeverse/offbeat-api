from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Place,SuggestedEdit
from .serializers import PlaceSerializer,SuggestedEditSerializer #for now I am not using the SuggestedEditSerializer to reduce complexity of the project
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

# here place details are sent from Backend to Frontend
@api_view(['GET'])
def get_place(request):
    query = request.GET.get('query', '').strip()
    if query:
        places = Place.objects.filter(title__istartswith=query)  # starts with, not contains
    else:
        places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)
    
# here place details are sent from Frontend to Backend
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_place(request):
    serializer = PlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
def list_all_places(request):
    from places.models import Place
    from places.serializers import PlaceSerializer
    search = request.GET.get('search', '')
    places = Place.objects.filter(name__icontains=search) if search else Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
