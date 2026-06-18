from django.shortcuts import render
from rest_framework import status
from places.models import Place
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import PlaceSerializer, ServiceSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from services.models import Service
from users.models import Provider
from reviews.models import Review


# ── Places: available to ALL logged-in users ──────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placesView(request):
    places = Place.objects.filter(created_by=request.user)
    serializer = PlaceSerializer(places, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def placeDetailView(request, pk):
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response({'detail': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Only the creator can edit/delete
    if request.method in ['DELETE', 'PUT', 'PATCH']:
        if place.created_by != request.user:
            return Response({'detail': 'You can only modify your own places.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = PlaceSerializer(place, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        place.delete()
        return Response({'message': 'Place deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method in ['PUT', 'PATCH']:
        serializer = PlaceSerializer(place, data=request.data, partial=(request.method == 'PATCH'), context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Services: providers only ──────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def servicesView(request):
    if request.user.role != 'service_provider':
        return Response({'detail': 'Only providers can access services.'}, status=status.HTTP_403_FORBIDDEN)

    provider = Provider.objects.get(user=request.user)
    services = Service.objects.filter(provider=provider)
    serializer = ServiceSerializer(services, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def serviceDetailView(request, pk):
    if request.user.role != 'service_provider':
        return Response({'detail': 'Only providers can access services.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({'detail': 'Service not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        service.delete()
        return Response({'message': 'Service deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ServiceSerializer(service, data=request.data, partial=(request.method == 'PATCH'), context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Reviews: all logged-in users ──────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReviews(request):
    reviews = Review.objects.filter(user_id=request.user)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)