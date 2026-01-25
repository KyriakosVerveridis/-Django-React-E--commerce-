from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product 
from base.products import products
from base.serializers import ProductSerializer


from django.contrib.auth.hashers import make_password
from rest_framework import status


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