from ..schemas.movie_schemas import (
    AvaliationSchema, MovieSchemaOut, MoviesListageQueryParams
    )
from ..models import Artist, Gender, Movie, Avaliation
from django.contrib.auth.models import User
from ninja.errors import HttpError
from django.db.models import Q

class MovieHandler:
    def __init__(self, request=None) -> None:
        self.request = request
        self.user: User = request.user
        
    
    def add_movie(self, movie: MovieSchemaOut) -> Movie:
        if not self.user or not self.user.is_superuser:
            raise HttpError(400, "Você precisa ser superuser")
        
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
            title=movie.title,
            year=movie.year, synopsis=movie.synopsis
        )
        movie_obj.directors.add(*directors)
        movie_obj.actors.add(*actors)
        movie_obj.genders.add(*genders)
        movie_obj.save()
        return MovieSchemaOut.from_movie(movie_obj)
    
    def avaliate_movie(self, avaliation: AvaliationSchema):
        
        if not self.user or self.user.is_superuser:
            raise HttpError(400, "Votos não podem ser feitos por superusers")
        avl_obj = Avaliation.objects.create(
            user=self.user ,**avaliation.model_dump()
        )
        movie_obj = avl_obj.movie
        movie_obj.calc_rates()
        return MovieSchemaOut.from_movie(movie_obj)
    
    def movies_listage(self, query: MoviesListageQueryParams):
        filters = Q()

        if query.director:
            filters &= Q(directors__name__icontains=query.director)
        if query.actor:
            filters &= Q(actors__name__icontains=query.actor)
        if query.gender:
            filters &= Q(genders__description__icontains=query.gender)
        if query.title:
            filters &= Q(title__icontains=query.title)
            
        movies = Movie.objects.filter(filters).order_by('rating', 'title')
        
        if query.paginated:
            start = (query.page - 1) * query.page_size
            end = start + query.page_size
            movies = movies[start:end]
        movies = [MovieSchemaOut.from_movie(movie) for movie in movies]
        return movies
    
    def get_movie_synopsis(self, movie_id):
        synopsis = Movie.objects.get(pk=movie_id).get_synopsis()
        return synopsis