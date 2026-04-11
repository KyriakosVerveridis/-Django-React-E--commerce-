from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product, Order

class OrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='buyer@test.com', password='password123')
        self.product = Product.objects.create(
            user=self.user, name='Camera', price=100, countInStock=10
        )
        self.order_data = {
            "orderItems": [{"product": self.product._id, "qty": 2, "price": 100}],
            "paymentMethod": "PayPal",
            "taxPrice": 0, "shippingPrice": 0, "totalPrice": 200,
            "shippingAddress": {"address": "123 St", "city": "Athens", "postalCode": "1", "country": "GR"}
        }

    def test_add_order_success(self):
        """Verify order creation and stock deduction"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/orders/add/', self.order_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.countInStock, 8)

    def test_update_order_to_paid(self):
        """Verify payment status update"""
        self.client.force_authenticate(user=self.user)
        order = Order.objects.create(user=self.user, totalPrice=200)
        
        response = self.client.put(f'/api/orders/{order._id}/pay/')
        order.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(order.isPaid)