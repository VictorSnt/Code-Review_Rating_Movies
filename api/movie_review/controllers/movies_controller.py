from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller
from ninja_extra import route
from ..schemas.movie_schemas import MovieSchemaOut
from ..models import Artist, Gender, Movie


@api_controller('movie', tags=['Movie'])
class MoviesController:
    @route.post('/register_movie', auth=JWTAuth())
    def register_movie(self, request: HttpRequest, movie: MovieSchemaOut):
        
        directors = [
            Artist.objects.get_or_create(**director.model_dump())[0]
            for director in movie.directors
        ]
        actors = [
            Artist.objects.get_or_create(**actor.model_dump())[0]
            for actor in movie.actors
        ]
        genders = [
            Gender.objects.get_or_create(**gender.model_dump())[0]
            for gender in movie.genders
        ]
        movie_obj = Movie.objects.create(
            year=movie.year, synopsis=movie.synopsis
        )
        movie_obj.directors.add(*directors)
        movie_obj.actors.add(*actors)
        movie_obj.genders.add(*genders)
        movie_obj.save()
        return MovieSchemaOut.from_movie(movie_obj)
