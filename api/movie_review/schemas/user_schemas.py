from ninja import Schema
from pydantic import BaseModel, Field

class UserSchema(Schema):
    username: str 
    password: str
    first_name: str
    last_name: str
    email: str
    is_active: bool 

class UpdateUserSchema(BaseModel):
    username: str = Field(None)
    password: str = Field(None)
    first_name: str = Field(None)
    last_name: str = Field(None)
    email: str = Field(None)
    first_name: str = Field(None)
    
    