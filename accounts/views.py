from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Register endpoint is live!'}, status=200)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User registered successfully!'}, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])  # No permissions required for login
def login_user(request):
    """Log in an existing user."""
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful!'}, status=200)
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def get_user_profile(request):
    """Retrieve the logged-in user's profile."""
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        return JsonResponse(serializer.data, status=200, safe=False)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def update_user_profile(request):
    """Update the logged-in user's profile."""
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        data = JSONParser().parse(request)
        serializer = UserProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Profile updated successfully!'}, status=200)
        return JsonResponse(serializer.errors, status=400)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

