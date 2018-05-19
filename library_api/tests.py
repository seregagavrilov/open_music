from django.urls import reverse
import requests
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.test import APITestCase, APIClient
from rest_framework.authentication import get_user_model
User = get_user_model()

class LibraryTestsCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'foo',
            'myemail@test.com',
            'pass'
        )

    def test_get_user_songs(self):
        """
        Ensure we can get songs from our REST API

        """

        self.client.login(username='foo', password='pass')
        response = self.client.get('/library_api/api_v1/usersongs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

