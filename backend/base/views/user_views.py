from django.shortcuts import render
from typing import Any

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.serializers import UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs) # Get standard tokens (access/refresh)
        
        # Serialize user object with our custom fields (name, isAdmin, etc.)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items(): # Loop through user data
            data[k] = v # Add each field to the final response

        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view (['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view (['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    """
    Updates the profile information of the currently authenticated user.
    """
    user = request.user # get authenticated user from request (via Token)
    serializer = UserSerializerWithToken(user, many=False)
    
    # request.data contains the parsed content of the request body (JSON sent from React)
    data = request.data

    user.first_name = data['name']
    user.email = data['email']
    user.username = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()

    return Response(serializer.data) # return data as a JSON object


@api_view (['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
    Returns the profile information of the currently authenticated user.
    """
    user = request.user # get authenticated user from request (via Token)
    serializer = UserSerializer(user, many=False) # serialize a single user object
    return Response(serializer.data) # return data as a JSON object


@api_view (['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)    