from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import json

class UserEndPointTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.default__user_data = {
            'username': 'admin',
            'password': 'admin',
        }
        self.test_user_data = {
            'username': 'test',
            'password': 'test',
        }
        get_user_model().objects.create_user(**self.default__user_data)
        self.admin_token = self.gen_user_token()
    
    def gen_user_token(self):
        data = self.default__user_data
        
        response = self.client.post(
            "/api/token/pair",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        return response.json() 
    
    def test_create_user(self):
        response = self.client.post(
            "/api/user/create_user",
            data=json.dumps(self.test_user_data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        
    def test_update_user(self):
        response = self.client.put(
            "/api/user/update_user",
            data=json.dumps({"first_name": "string",}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        first_name = response.json()['first_name']
        self.assertEqual(first_name, 'string')
    
    def test_update_user_password(self):
        response = self.client.put(
            f"/api/user/change_user_password?newpassword=1234",
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        
        
    def test_deactivate_user(self):
        get_user_model().objects.create(username='str', password='str')
        response = self.client.delete(
            f"/api/user/deactivate_user",
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
