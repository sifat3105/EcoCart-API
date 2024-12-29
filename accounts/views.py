from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import UserProfile
from .serializers import LoginSerializer, UserProfileSerializer, UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
class UpdateUserProfileView(UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if request.user.is_authenticated:
            if request.user.username != username:
                return Response({"message": "Username is not match"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        return user_profile

    def post(self, request, *args, **kwargs):
        instance = self.get_object
        serializer = self.get_serializer(instance, self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

