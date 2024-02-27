from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller
from ninja_extra import route
from ..schemas.movie_schemas import (
    MovieSchemain, AvaliationSchema, MoviesListageQueryParams)
from ..services.movie_handler import MovieHandler
from ninja import Query


@api_controller('movie', tags=['Movie'])
class MoviesController:
    handler_class = MovieHandler
    
    @route.get('/movies_listage', auth=JWTAuth())
    def movies_listage(self, request: HttpRequest, query: Query[MoviesListageQueryParams]):
        self.handler = self.handler_class(request)
        return self.handler.movies_listage(query)
    
    @route.get('/get_movie_synopsis', auth=JWTAuth())
    def get_movie_synopsis(self, request: HttpRequest, movie_id: str):
        self.handler = self.handler_class(request)
        return self.handler.get_movie_synopsis(movie_id)
    
    @route.post('/register_movie', auth=JWTAuth())
    def register_movie(self, request: HttpRequest, movie: MovieSchemain):
        self.handler = self.handler_class(request)
        return self.handler.add_movie(movie)
    
    @route.post('/avaliate_movie', auth=JWTAuth())
    def avaliate_movie(self, request: HttpRequest, vote: AvaliationSchema):
        self.handler = self.handler_class(request)
        return self.handler.avaliate_movie(vote)