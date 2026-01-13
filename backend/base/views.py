from typing import Any
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product 
from .products import products
from .serializers import ProductSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        data["username"] = self.user.username
        data["email"] = self.user.email

        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view (['GET'])
def getRouter(request):
    
    return Response("Hello")


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