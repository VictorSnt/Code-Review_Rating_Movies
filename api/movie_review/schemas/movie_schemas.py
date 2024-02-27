from uuid import UUID
from ninja import Schema
from typing import List
from datetime import date
from pydantic import BaseModel
from.pagination_schema import PaginationSchema


class ArtistSchema(BaseModel):
    name: str

class GenderSchema(BaseModel):
    description: str


    
class AvaliationSchema(BaseModel):
    rate: int
    movie_id: UUID
    
class MovieSchemain(Schema):
    title: str
    year: date
    synopsis: str
    actors: List[ArtistSchema]
    directors: List[ArtistSchema]
    genders: List[GenderSchema]

class MovieSchemaOut(MovieSchemain):
    id: UUID

    @classmethod
    def from_movie(cls, movie):
        actors = [
            {"id": str(actor.id), "name": actor.name}
            for actor in movie.actors.all()
        ]
        directors = [
            {"id": str(director.id), "name": director.name}
            for director in movie.directors.all()
        ]
        genders = [
            {"id": str(gender.id), "description": gender.description}
            for gender in movie.genders.all()
        ]
        
        return cls(
            id=str(movie.id),
            title=movie.title,
            year=movie.year,
            synopsis=movie.get_synopsis(),
            actors=actors,
            directors=directors,
            genders=genders,
            created_at=movie.created_at,
            updated_at=movie.updated_at
        )

class MovieListSchemain(Schema):
    movies: List[MovieSchemaOut]
    
class MoviesListageQueryParams(PaginationSchema):
    director: str = ''
    actor: str = ''
    gender: str = ''
    title: str = ''