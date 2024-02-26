from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import route
from ..schemas.user_schemas import (
    ResponseUserSchema,CreateUserSchema, UpdateUserSchema
)

class BaseUserController:
    handler_class = None

    
    @route.post('/create', response=ResponseUserSchema, auth=JWTAuth()) 
    def create(self, user_in: CreateUserSchema):
        self.handler = self.handler_class()
        response = self.handler.create_user(user_schema=user_in)
        return response
    
    @route.put('/update', response=ResponseUserSchema, auth=JWTAuth())
    def update(self, request: HttpRequest, user_in: UpdateUserSchema):
        self.handler = self.handler_class(request)
        response = self.handler.update_user(user_schema=user_in)
        return response
    
    @route.put('changepassword', response=ResponseUserSchema, auth=JWTAuth())
    def change_password(self, request: HttpRequest, newpassword: str):
        self.handler = self.handler_class(request)
        response = self.handler.change_password(newpassword=newpassword)
        return response
    
    @route.delete('/deactivate', response=ResponseUserSchema, auth=JWTAuth())
    def inativate_user(self, request: HttpRequest):
        self.handler = self.handler_class(request)
        response = self.handler.inativate_user()
        return response
    