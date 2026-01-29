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


@api_view (['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    try:
        # Fetch the user by primary key
        user = User.objects.get(id=pk)
        data = request.data

        # If a field is missing from the request, use the current user value as a fallback
        user.first_name = data.get('name', user.first_name)
        user.email = data.get('email', user.email)
        user.username = data.get('email', user.username) # Syncing username with email
        user.is_staff = data.get('isAdmin', user.is_staff)

        user.save()
        
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        # Return 404 if the user ID is invalid
        return Response(
            {'detail': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Catch any other unexpected errors to prevent a 500 status code
        return Response(
            {'detail': f'An error occurred: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view (['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    try:
        # Attempt to find the user by primary key (id)
        userForDelete = User.objects.get(id=pk)
        userForDelete.delete()
        return Response({'detail': 'User was deleted successfully'}, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        # Handle the case where the user ID is not found in the database
        return Response(
            {'detail': 'User with this ID does not exist'}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
    except Exception as e:
        # Catch any other unexpected errors
        return Response(
            {'detail': f'An unexpected error occurred: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )