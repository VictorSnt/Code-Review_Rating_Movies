from pydantic import BaseModel, Field
from ninja.errors import HttpError
from ninja import Schema

class ResponseUserSchema(Schema):
    username: str 
    password: str
    first_name: str
    last_name: str
    email: str
    
class UserBaseSchema(BaseModel):
    def remove_null_fields(self):
        schema_dict = self.model_dump()
        filtered_fields = {
            key: schema_dict[key] for key in schema_dict.keys()
            if schema_dict[key]
        }
        if not filtered_fields:
            raise HttpError(400, "Nenhum campo valido foi preenchido") 
        return filtered_fields
    
class UpdateUserSchema(UserBaseSchema):
    username: str = Field(None)
    first_name: str = Field(None)
    last_name: str = Field(None)
    email: str = Field(None)

class CreateUserSchema(UserBaseSchema):
    username: str 
    password: str
    first_name: str = Field(None)
    last_name: str = Field(None)
    email: str = Field(None)
    is_active: bool  = Field(True)

    