from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# gets data from backend to frontend
@api_view(['GET'])
def get_reviews(request,place_id):
    reviews = Review.objects.filter(place_id=place_id)
    serializer=ReviewSerializer(reviews,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    serializer=ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, id):
    # 1. Get the review
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    # 2. Check if logged-in user is the creator
    if review.user_id != request.user:
        return Response({'error': 'You are not allowed to delete this review'},
                        status=status.HTTP_403_FORBIDDEN)

    # 3. Delete
    review.delete()
    return Response({'message': 'Review deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, id):
    # 1. Find the review
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    # 2. Check if the logged-in user is the creator
    if review.user_id != request.user:
        return Response({'error': 'You are not allowed to update this review'}, 
                        status=status.HTTP_403_FORBIDDEN)

    # 3. Update the review
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()   # created_by remains same automatically
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
