from django.contrib.auth.models import User
from django.test import TestCase, Client
import json


class TestAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.super_default_user_data = {
            'username': 'admin',
            'password': 'admin',
        }
        self.test_superuser_data = {
            'username': 'supertest',
            'password': 'supertest',
        }
        self.test_user_data = {
            'username': 'test',
            'password': 'test',
        }
        User.objects.create_superuser(**self.super_default_user_data)

    def test_get_token(self, creds=False):
        if not creds:
            data = self.super_default_user_data
        else: 
            data = creds
        response = self.client.post(
            "http://127.0.0.1:8000/api/token/pair",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        return response.json()['access'] 

    def test_create_user(self):
        token = self.test_get_token(self.super_default_user_data)
        response = self.client.post(
            "http://127.0.0.1:8000/api/superuser/create_superuser",
            data=json.dumps(self.test_superuser_data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        self.assertEqual(response.status_code, 200)
        new_user = User.objects.get(
            username=self.test_superuser_data['username'])
        self.assertEqual(new_user.is_superuser, True)