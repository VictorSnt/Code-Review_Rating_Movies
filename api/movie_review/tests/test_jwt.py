from django.contrib.auth import get_user_model
from django.test import TestCase, Client

class JWTEndPointTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.default_super_user_data = {
            'username': 'admin',
            'password': 'admin',
        }
        get_user_model().objects.create_superuser(**self.default_super_user_data)

    def test_gen_user_token(self):
        data = self.default_super_user_data
        response = self.client.post(
            "/api/token/pair",
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        return response.json() 

    def test_refresh_user_token(self):
        token = self.test_gen_user_token()
        response = self.client.post(
            "/api/token/refresh",
            data={'refresh': token['refresh']},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_verify_user_token(self):
        token = self.test_gen_user_token()
        response = self.client.post(
            "/api/token/verify",
            data={'token': token['access']},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
