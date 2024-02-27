from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.description
 
class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=45, null=False, default="None", unique=True)
    actors = models.ManyToManyField(
        Artist, related_name='acted_in_movies', verbose_name='Ator')
    directors = models.ManyToManyField(
        Artist, related_name='directed_movies', verbose_name='Diretor')
    rating =  models.FloatField(null=True, default=None, verbose_name='Nota')
    genders = models.ManyToManyField(Gender, verbose_name='Gênero')
    year = models.DateField(null=False, verbose_name='Ano')
    synopsis = models.TextField(null=False, verbose_name='Sinopse')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_synopsis(self) -> None:
        rating = self.rating or 'sem avaliações!'
        if not rating:
            ValueError('Rating should not be null|False')
        return f'Titulo: {self.title} Nota: {rating}\n {self.synopsis}'

    def calc_rates(self) -> None:
        rates = [vote.rate for vote in self.votations.all()]
        self.rating = sum(rates) / len(rates)
        self.save()
        
    def __str__(self) -> str:
        return (f'Title: {self.title}'
        f'actors: {[actor for actor in self.actors.all()]}'
        f'directors: {[director for director in self.directors.all()]}')
        
class Avaliation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='votes')
    movie = models.ForeignKey(
        Movie, on_delete=models.PROTECT, related_name='votations')
    rate = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.rate < 0 or self.rate > 4:
            raise ValueError("A taxa deve estar entre 0 e 4.")
        if self.movie_id is not None and not self.movie:
            self.movie = Movie.objects.get(pk=self.movie_id)
        super().save(*args, **kwargs)