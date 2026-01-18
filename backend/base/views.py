from typing import Any
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Product 
from django.contrib.auth.models import User
from .products import products
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.


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

@api_view (['GET'])
def getRouter(request):
    
    return Response("Hello")


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
def getProducts(request):
    """
    Function to fetch all products.
    """
    products = Product.objects.all() # get all products from DB
    serializer = ProductSerializer(products, many=True) # serialize a list of objects
    return Response(serializer.data)


@api_view (['GET'])
def getProduct(request, pk):
    """
    Function to fetch a specific product by ID.
    """
    product = Product.objects.get(_id=pk) # get product from DB
    serializer = ProductSerializer(product, many=False) # serialize a single object
    return Response(serializer.data)