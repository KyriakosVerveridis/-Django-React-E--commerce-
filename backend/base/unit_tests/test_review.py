from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product, Review

class ReviewTests(APITestCase):

    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(username='tester', password='password123')
        
        # Create a product to review
        self.product = Product.objects.create(
            user=self.user,
            name='Test Watch',
            price=100.00,
            brand='Apple',
            countInStock=5
        )
        
        # Consistent URL based on your product_urls.py
        self.url = f'/api/products/{self.product._id}/review/'

    def test_create_review_success(self):
        """Test successful review creation and product stats update"""
        self.client.force_authenticate(user=self.user)
        data = {
            'rating': 4,
            'comment': 'Great product!'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        
        # Ensure the product reflects the new review
        self.product.refresh_from_db()
        self.assertEqual(self.product.numReviews, 1)

    def test_duplicate_review_fails(self):
        """Test that a user cannot review the same product more than once"""
        self.client.force_authenticate(user=self.user)
        
        # Submit the first review
        self.client.post(self.url, {'rating': 5, 'comment': 'First review'}, format='json')
        
        # Attempt to submit a second review for the same product
        response = self.client.post(self.url, {'rating': 1, 'comment': 'Second review'}, format='json')
        
        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Product already reviewed')

    def test_zero_rating_fails(self):
        """Test that a review with 0 rating is rejected by the logic"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'rating': 0,
            'comment': 'Bad rating'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        # Should return 400 Bad Request as rating must be > 0
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)