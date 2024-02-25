from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller, route
from ..services.user_handler import SuperUserHandler, UserHandler
from ..schemas.user_schemas import (
    ResponseUserSchema, CreateUserSchema, UpdateUserSchema
)

@api_controller('user', tags=['User'])
class UserController:
    
    @route.post('/create', response=ResponseUserSchema) 
    def create(self, user_in: CreateUserSchema):
        handler = UserHandler()
        response = handler.create_user(user_schema=user_in)
        return response
    
    @route.put('/update', response=ResponseUserSchema, auth=JWTAuth())
    def update(self, request: HttpRequest, user_in: UpdateUserSchema):
        handler = UserHandler(request)
        response = handler.update_user(user_schema=user_in)
        return response
    
    @route.put('changepassword', response=ResponseUserSchema, auth=JWTAuth())
    def change_password(self, request: HttpRequest, newpassword: str):
        handler = UserHandler(request)
        response = handler.change_password(newpassword=newpassword)
        return response
    
    @route.delete('/deactivate', response=ResponseUserSchema, auth=JWTAuth())
    def inativate_user(self, request: HttpRequest):
        handler = UserHandler(request)
        response = handler.inativate_user()
        return response
    
@api_controller('superuser', tags=['SuperUser'])
class SuperUserController(UserController):
    @route.get('/get_users', response=list[ResponseUserSchema], auth=JWTAuth())
    def get_users(self):
        handler = SuperUserHandler()
        response = handler.get_users()
        return response
    @route.post('/create', response=ResponseUserSchema, auth=JWTAuth()) 
    def create(self, user_in: CreateUserSchema):