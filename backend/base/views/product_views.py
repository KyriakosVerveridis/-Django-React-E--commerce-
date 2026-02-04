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


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    product = Product.objects.get(_id=pk)
    data = request.data

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.brand = data.get('brand', product.brand)
    product.countInStock = data.get('countInStock', product.countInStock)
    product.category = data.get('category', product.category)
    product.description = data.get('description', product.description)

    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view (['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    data = request.data

    product = Product.objects.create(
        user=user,
        name=data.get('name', 'Default Name'),
        price=data.get('price', 0),
        brand=data.get('brand', 'Default Brand'),
        countInStock=data.get('countInStock', 0),
        category=data.get('category', 'Default Category'),
        description=data.get('description', '')
    )
    
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view (['DELETE'])
@permission_classes([IsAdminUser])  
def deleteProduct(request, pk):
    """
    Function to delete a specific product by ID.
    """
    productToDelete = Product.objects.get(_id=pk)
    productToDelete.delete()
    
    return Response('Product deleted')


@api_view (['POST'])
@permission_classes([IsAdminUser]) 
def uploadImage(request):
    """
    Function to handle image upload for products.
    """
    data = request.data

    product_id = data.get('product_id')
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')
