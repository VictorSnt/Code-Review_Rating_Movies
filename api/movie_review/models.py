from django.db import models
import uuid

class Artist(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=50, 
        null=False, 
        unique=True, 
        verbose_name='Nome'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Gender(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=25, null=False, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Descrição'
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.description
    
class Movie(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=45, null=False, default="None")
    actors = models.ManyToManyField(
        Artist, related_name='acted_in_movies', verbose_name='Ator')
    directors = models.ManyToManyField(
        Artist, related_name='directed_movies', verbose_name='Diretor')
    rating =  models.FloatField(null=True, default=0, verbose_name='Nota')
    genders = models.ManyToManyField(Gender, verbose_name='Gênero')
    year = models.DateField(null=False, verbose_name='Ano')
    synopsis = models.TextField(null=False, verbose_name='Sinopse')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def add_rating_in_synopsis(self) -> None:
        rating = self.rating
        if not rating:
            ValueError('Rating should not be null|False')
        self.synopsis = f'Nota: {rating} {self.synopsis}'

    def __str__(self) -> str:
        return f'actors: {[actor for actor in self.actors.all()]}directors: {[director for director in self.directors.all()]}'