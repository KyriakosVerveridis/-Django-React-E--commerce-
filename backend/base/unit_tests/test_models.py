from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a product for testing
        self.product = Product.objects.create(
            user=self.user,
            name='Test Product',
            price=10.99,
            brand='Test Brand',
            category='Test Category',
            description='This is a test product.',
            countInStock=100
        )

    def test_product_creation(self):
        """
        Test that the product is created correctly.
        """
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 10.99)
        self.assertEqual(self.product.brand, 'Test Brand')
        self.assertEqual(self.product.category, 'Test Category')
        self.assertEqual(self.product.description, 'This is a test product.')
        self.assertEqual(self.product.countInStock, 100)

    def test_review_creation(self):
        """
        Test that a review can be created for the product.
        """
        review = self.product.review_set.create(
            user=self.user,
            name='Test Review',
            rating=5,
            comment='This is a test review.'
        )
        self.assertEqual(review.name, 'Test Review')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'This is a test review.')  

    def test_product_str(self):
        """
        Test the string representation of the product.
        """
        self.assertEqual(str(self.product), 'Test Product')    