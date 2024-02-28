from django.contrib.auth import get_user_model
from ..models import Movie, Artist, Gender, Avaliation
from django.test import TestCase, Client
import json

class MovieEndPointTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.default_super_user_data = {
            'username': 'admin',
            'password': 'admin',
        }
        self.test_user_data = {
            'username': 'test',
            'password': 'test',
        }
        get_user_model().objects.create_superuser(
            **self.default_super_user_data)
        get_user_model().objects.create_user(
            **self.test_user_data)
        self.admin_token = self.gen_admin_token()
        self.user_token = self.gen_user_token()
        self.movie_id = self.movies_registration()
    
    def gen_user_token(self):
        response = self.client.post(
            "/api/token/pair",
            data=json.dumps(self.test_user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        return response.json() 
    
    def gen_admin_token(self):
        response = self.client.post(
            "/api/token/pair",
            data=json.dumps(self.default_super_user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        return response.json() 
    
    def movies_registration(self):
        movies = [
        {
            "title": "Saving Private Ryan",
            "year": "1998-07-24",
            "synopsis": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
            "actors": [{"name": "Tom Hanks"}],
            "directors": [{"name": "Steven Spielberg"}],
            "genders": [{"description": "Drama"}]
        },
        {
            "title": "Fight Club",
            "year": "1999-10-15",
            "synopsis": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.",
            "actors": [{"name": "Brad Pitt"}],
            "directors": [{"name": "Christopher Nolan"}],
            "genders": [{"description": "Action"}]
        }
    ]
    
        for movie in movies:
            response = self.client.post(
                '/api/movie/register_movie',
                data=json.dumps(movie),
                content_type='application/json',
                HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access']
            )
            self.assertEqual(response.status_code, 200)
        return response.json()['id']
    
    def test_movie_get_synopsi(self):
        id = self.movie_id
        
        response = self.client.get(
            '/api/movie/get_movie_synopsis?movie_id={}'.format(id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_avaliate_movie(self):
        response = self.client.post(
            '/api/movie/avaliate_movie',
            data=json.dumps({'movie_id': self.movie_id, 'rate': 4}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        
    def test_movie_listage_all(self):
        response = self.client.get(
            '/api/movie/movies_listage',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['id'], self.movie_id)
    
    def test_movie_listage_paged_by_one(self):
        response = self.client.get(
            '/api/movie/movies_listage?paginated=true&page_size=1',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
    
    def test_movie_listage_by_title(self):
        response = self.client.get(
            '/api/movie/movies_listage?title=Saving Private Ryan',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_movie_listage_by_director(self):
        response = self.client.get(
            '/api/movie/movies_listage?director=Steven Spielberg',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_movie_listage_by_gender(self):
        response = self.client.get(
            '/api/movie/movies_listage?gender=Action',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_movie_listage_by_actor(self):
        response = self.client.get(
            '/api/movie/movies_listage?actor=Brad Pitt',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token['access']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)