from ninja import Schema
from typing import List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class ArtistSchema(BaseModel):
    name: str

class GenderSchema(BaseModel):
    description: str

class MovieSchemaOut(Schema):
    title: str
    year: date
    synopsis: str
    actors: List[ArtistSchema]
    directors: List[ArtistSchema]
    genders: List[GenderSchema]


    @classmethod
    def from_movie(cls, movie):
        actors = [ArtistSchema(id=actor.id, name=actor.name) for actor in movie.actors.all()]
        directors = [ArtistSchema(id=director.id, name=director.name) for director in movie.directors.all()]
        genders = [GenderSchema(id=gender.id, description=gender.description) for gender in movie.genders.all()]
        return cls(
            id=movie.id,
            year=movie.year,
            synopsis=movie.synopsis,
            actors=actors,
            directors=directors,
            genders=genders,
            created_at=movie.created_at,
            updated_at=movie.updated_at
        )
