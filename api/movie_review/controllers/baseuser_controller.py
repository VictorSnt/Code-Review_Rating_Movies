from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import route
from ..schemas.user_schemas import (
    ResponseUserSchema,CreateUserSchema, UpdateUserSchema
)

class BaseUserController:
    def __init__(self, handler_class):
        self.handler_class = handler_class

    @route.post('/create_user', response=ResponseUserSchema, auth=JWTAuth()) 
    def create_user(self, user_in: CreateUserSchema):
        self.handler = self.handler_class()
        response = self.handler.create_user(user_schema=user_in)
        return response
    
    @route.put('/update_user', response=ResponseUserSchema, auth=JWTAuth())
    def update_user(self, request: HttpRequest, user_in: UpdateUserSchema):
        self.handler = self.handler_class(request)
        response = self.handler.update_user(user_schema=user_in)
        return response
    
    @route.put('change_user_password', response=ResponseUserSchema, auth=JWTAuth())
    def change_user_password(self, request: HttpRequest, newpassword: str):
        self.handler = self.handler_class(request)
        response = self.handler.change_password(newpassword=newpassword)
        return response
    
    @route.delete('/deactivate_user', response=ResponseUserSchema, auth=JWTAuth())
    def deactivate_user(self, request: HttpRequest):
        self.handler = self.handler_class(request)
        response = self.handler.deactivate_user()
        return response
    