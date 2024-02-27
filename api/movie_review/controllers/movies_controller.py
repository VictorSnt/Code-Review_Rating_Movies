from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller
from ninja_extra import route
from ..schemas.movie_schemas import (
    MovieSchemain, AvaliationSchema)
from ..services.movie_handler import MovieHandler

@api_controller('movie', tags=['Movie'])
class MoviesController:
    handler_class = MovieHandler
    
    @route.post('/register_movie', auth=JWTAuth())
    def register_movie(self, request: HttpRequest, movie: MovieSchemain):
        self.handler = self.handler_class(request)
        return self.handler.add_movie(movie)
    
    @route.post('/avaliate_movie', auth=JWTAuth())
    def avaliate_movie(self, request: HttpRequest, vote: AvaliationSchema):
        self.handler = self.handler_class(request)
        return self.handler.avaliate_movie(vote)