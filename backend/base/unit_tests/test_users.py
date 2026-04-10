from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_register_user(self):
        """
        Test that a user can be registered successfully.
        """
        url = '/api/users/register/'
        data = {
            'name': 'Giannis',
            'email': 'giannis@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains the right data
        self.assertEqual(response.data['email'], 'giannis@example.com')
        self.assertIn('token', response.data)

    def test_user_login(self):
        """
        Test that a user can log in successfully.
        """
        User.objects.create_user(username='giannis@example.com', email='giannis@example.com', password='password123')
        
        url = '/api/users/login/'
        data = {
            'username': 'giannis@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_user_profile_authorized(self):
        """
        Test that an authenticated user can access their profile information.
        """
        # Create a user for testing
        user = User.objects.create_user(
            username='test@test.com', 
            email='test@test.com', 
            password='password123'
        )
        
        # Manually authenticate the user for the API client
        self.client.force_authenticate(user=user)
        
        url = '/api/users/profile/'
        response = self.client.get(url)
        
        # Check that the response is successful and returns the correct email
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')