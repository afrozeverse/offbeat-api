from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import RegisterSerializer, ProfileSerializer,ProviderSerializer
from .models import Customer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import Provider
from rest_framework.decorators import api_view, permission_classes
import json
from .models import Customer,Provider
# Registerview runs when the frontend sends a POST request (signup form).
class Registerview(APIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'message': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)


from rest_framework.parsers import MultiPartParser, FormParser

class BecomeProviderView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # For file upload
    
    def post(self, request):
        user = request.user
        
        # Check if already a provider
        if user.role == 'service_provider':
            return Response({
                'message': 'You are already a service provider',
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if Provider profile already exists
        if hasattr(user, 'provider_profile'):
            return Response({
                'message': 'Provider profile already exists',
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get form data
        display_name = request.data.get('display_name')
        about = request.data.get('about', '')
        contact_phone = request.data.get('contact_phone')

        services_offered = request.data.get('services_offered', '[]')

        try:
            services_offered = json.loads(services_offered)
        except json.JSONDecodeError:
            services_offered = []
        docs = request.FILES.get('docs')  # File upload
        
        # Validate required fields
        if not display_name or not contact_phone:
            return Response({
                'message': 'Display name and phone are required',
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update user role
        user.role = 'service_provider'
        user.save()
        
        # Create Provider profile
        provider = Provider.objects.create(
            user=user,
            display_name=display_name,
            about=about,
            contact_phone=contact_phone,
            services_offered=services_offered if isinstance(services_offered, list) else [],
            docs=docs
        )
        
        return Response({
            'message': 'Successfully upgraded to service provider!',
            'status': True,
            'provider': {
                'id': str(provider.id),
                'display_name': provider.display_name,
                'about': provider.about,
                'verified': provider.verified
            },
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

@api_view(['DELETE'])
def manage_account(request,id):
    try:
        user=Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        if user.id != request.user.id:
            return Response(
                {"error": "You do not have permission to delete this account."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Perform deletion
        user.delete()
        
        # Return 204 No Content (standard for successful DELETE requests)
        return Response(
            {"message": "Account deleted successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
    # ── Add this to users/views.py ──────────────────────────────────────────

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Provider, Customer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_providers(request):
    providers = Provider.objects.select_related('user').all()
    data = []
    for p in providers:
        data.append({
            "id": str(p.id),
            "display_name": p.display_name,
            "about": p.about,
            "contact_phone": p.contact_phone,
            "services_offered": p.services_offered,
            "verified": p.verified,
            "docs": request.build_absolute_uri(p.docs.url) if p.docs else None,
            "user": {
                "id": str(p.user.id),
                "username": p.user.username,
                "email": p.user.email,
                "phone": p.user.phone,
                "avatar": request.build_absolute_uri(p.user.avatar.url) if p.user.avatar else None,
            }
        })
    return Response(data)

@api_view(['GET'])
def get__provider(request,pk):
    try:
        provider=Provider.objects.get(pk=pk)
    except Provider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ProviderSerializer(provider)
    return Response(serializer.data,status=status.HTTP_200_OK)