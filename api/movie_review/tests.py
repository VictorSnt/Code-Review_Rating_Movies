from email.policy import default
from urllib import request
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json

class UserRoutesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        self.user = self.create_and_authenticate_user()

    def create_and_authenticate_user(self):
        # Cria o usuário
        response = self.client.post(
            '/api/user/create', 
            data=json.dumps(self.user_data), 
            content_type='application/json'
        )
       
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(username=self.user_data["username"])
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.user_data["username"])

        # Autentica o usuário e obtém o token
        response = self.client.post(
            '/api/token/pair', 
            data=json.dumps(self.user_data), 
            content_type='application/json'
        )
        self.token = response.json()['access']

        return user

    def test_change_password(self):
        # Testa a mudança de senha
        response = self.client.put(
            '/api/user/changepassword?newpassword=sucesses',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(username=self.user_data["username"])
        password_changed = get_user_model().check_password(user, 'sucesses')
        self.assertEqual(password_changed, True)

    def test_update_user(self):
        # Testa a atualização do usuário
        response = self.client.put(
            '/api/user/update', 
            data=json.dumps({'first_name': 'sucesses'}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.token
        ) 
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(username=self.user_data["username"])
        self.assertEqual(user.first_name, 'sucesses')

    def test_deactivate_user(self):
        # Testa a desativação do usuário
        response = self.client.delete(
            '/api/user/deactivate',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.assertEqual(response.status_code, 200)

class GetUsersList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user_data = {
            "username": "testsuperuser",
            "password": "testpassword123",
        }
        cls.default_admin = {
            "username": "admin",
            "password": "admin",
        }
        cls.create_superuser()
        cls.authenticate_superuser()
        cls.create_test_user()

    @classmethod
    def create_superuser(cls):
        get_user_model().objects.create_superuser(**cls.default_admin)

    @classmethod
    def authenticate_superuser(cls):
        response = cls.client.post(
            '/api/token/pair', 
            data=json.dumps(cls.default_admin), 
            content_type='application/json'
        )
        assert response.status_code == 200
        cls.token = response.json()['access']

    @classmethod
    def create_test_user(cls):
        response = cls.client.post(
            '/api/superuser/create', 
            data=json.dumps(cls.user_data), 
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + cls.token
        )
        assert response.status_code == 200

    @classmethod
    def create_test_users(cls):
        user_data_list = [
            {"username": f"testuser{i}", "password": "testpassword123"}
            for i in range(10)
        ]
        users = [get_user_model()(**data) for data in user_data_list]
        get_user_model().objects.bulk_create(users)
    
    def test_user_listage(self):
        self.create_test_users()
        response = self.client.get(
            '/api/superuser/get_users',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_user_listage_paginated(self):
        self.create_test_users()
        response = self.client.get(
            f'/api/superuser/get_users?paginated=true&page_size=2',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

        
    
    

