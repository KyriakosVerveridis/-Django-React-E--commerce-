from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Product, Review 
from base.products import products
from base.serializers import ProductSerializer


from django.contrib.auth.hashers import make_password
from rest_framework import status


@api_view (['GET'])
def getProducts(request):
    """
    Endpoint to fetch all products.
    """
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Product.objects.filter(name__icontains=query) # get products from DB with name containing the query

    page = request.query_params.get('page')
    paginator = Paginator(products, 2) # paginate the products, 2 per page

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1) # if page is not an integer, return the first page
    except EmptyPage:
        products = paginator.page(paginator.num_pages) # if page is out of range, return the last page

    if page == None:
        page = 1    
    page = int(page)

    serializer = ProductSerializer(products, many=True)
    return Response({
        'products': serializer.data,
        'page': page,
        'pages': paginator.num_pages
    })

@api_view (['GET'])
def getTopProducts(request):
    """
    Endpoint to fetch top rated products.
    """
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5] # get top 5 products ordered by rating
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view (['GET'])
def getProduct(request, pk):
    """
    Endpoint to fetch a specific product by ID.
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
    Endpoint to delete a specific product by ID.
    """
    productToDelete = Product.objects.get(_id=pk)
    productToDelete.delete()
    
    return Response('Product deleted')


@api_view (['POST'])
@permission_classes([IsAdminUser]) 
def uploadImage(request):
    """
    Endpoint to handle image upload for products.
    """
    data = request.data

    product_id = data.get('product_id')
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response({'message': 'Image was uploaded', 'image_url': product.image.url})


@api_view (['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request,pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 2 - No rating or 0 rating
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],    
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()
        return Response('Review Added')

