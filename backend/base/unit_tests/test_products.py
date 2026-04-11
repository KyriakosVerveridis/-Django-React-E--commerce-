from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product

from django.core.exceptions import ValidationError

class ProductViewsTest(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some products for testing
        self.product1 = Product.objects.create(
            user=self.user,
            name='Test Product 1',
            price=10.99,
            brand='Test Brand',
            category='Test Category',
            description='This is the first test product.',
            countInStock=100
        )
        self.product2 = Product.objects.create(
            user=self.user,
            name='Test Product 2',
            price=20.99,
            brand='Test Brand',
            category='Test Category',
            description='This is the second test product.',
            countInStock=50
        )

    def test_get_products(self):
        """
        Test that we can retrieve a list of products.
        """
        url = '/api/products/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 2)

    def test_get_product_by_id(self):
        """
        Test that we can retrieve a product by its ID.
        """
        url = f'/api/products/{self.product1._id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product 1')

    def test_delete_product_as_admin_user(self):
            """
            Test that an admin user can delete a product.
            """
            self.client.force_authenticate(user=self.admin_user)
            url = f'/api/products/delete/{self.product1._id}/'
            response = self.client.delete(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertFalse(Product.objects.filter(_id=self.product1._id).exists())        

    def test_delete_product_as_user_fails(self):
            """
            Test that a non-admin user cannot delete a product.
            """
            self.client.force_authenticate(user=self.user)
            url = f'/api/products/delete/{self.product2._id}/'
            response = self.client.delete(url)
            
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertTrue(Product.objects.filter(_id=self.product2._id).exists())

    def test_product_negative_price(self):
        """
        Test that a product cannot have a negative price.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = '/api/products/create/'
        data = {
            'name': 'Invalid Product',
            'price': -5.99,
            'brand': 'Test Brand',
            'category': 'Test Category',
            'description': 'This product has an invalid price.',
            'countInStock': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
       