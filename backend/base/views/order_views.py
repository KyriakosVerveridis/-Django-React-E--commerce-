from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from django.utils import timezone


@api_view (['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    """
    Function to add order items to the database.
    """
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Create order
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # Create shipping address
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        # Create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )

            # Update stock
            product.countInStock -= item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    

@api_view (['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)   


@api_view (['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    """
    Function to fetch all orders.
    """
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
    

@api_view (['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    """
    Function to get order by ID.
    """
    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        # Check if user is admin or owner of the order
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_403_FORBIDDEN)
    except Order.DoesNotExist:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view (['PUT'])
@permission_classes([IsAuthenticated])    
def updateOrderToPaid(request, pk):
    try:
        # 1. Fetch the order by primary key
        order = Order.objects.get(_id=pk)
        
        # 2. Check if the authenticated user owns this order
        if order.user != request.user:
            return Response(
                {'detail': 'Not authorized to view this order'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Update payment status
        order.isPaid = True
        order.paidAt = timezone.now()
        order.save()

        # 4. Return the updated order object
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

    except Order.DoesNotExist:
        # If order ID is not found
        return Response(
            {'detail': 'Order does not exist'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        # Handle any other unexpected errors
        return Response(
            {'detail': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )