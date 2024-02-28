from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import json

class SuperUserEndPointTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.default_super_user_data = {
            'username': 'admin',
            'password': 'admin',
        }
        self.test_superuser_data = {
            'username': 'supertest',
            'password': 'supertest',
        }
        get_user_model().objects.create_superuser(**self.default_super_user_data)
        self.admin_token = self.gen_user_token()
    
    def gen_user_token(self):
        data = self.default_super_user_data
        
        response = self.client.post(
            "/api/token/pair",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        return response.json() 
    
    
    def test_create_superuser(self):
        response = self.client.post(
            "/api/superuser/create_superuser",
            data=json.dumps(self.test_superuser_data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        is_superuser = response.json()['is_superuser']
        self.assertEqual(is_superuser, True)
    
    def test_update_superuser(self):
        response = self.client.put(
            "/api/superuser/update_superuser",
            data=json.dumps({"first_name": "string",}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        first_name = response.json()['first_name']
        self.assertEqual(first_name, 'string')
    
    def test_update_superuser_password(self):
        response = self.client.put(
            f"/api/superuser/change_superuser_password?newpassword=1234",
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        
        
    def test_deactivate_superuser(self):
        get_user_model().objects.create(username='str', password='str')
        response = self.client.delete(
            f"/api/user/deactivate_user",
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)

    def test_users_listage(self):
        get_user_model().objects.bulk_create(
            [get_user_model()(**{
                'username':f'user{number}',
                'password':'123456'
            })for number in range(30)])
        
        response = self.client.get(
            f"/api/superuser/get_users",
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            f"/api/superuser/get_users?paginated=True",
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)