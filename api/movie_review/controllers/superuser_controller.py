from django.http import HttpRequest
from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller, route
from ..controllers.baseuser_controller import BaseUserController
from ..services.superuser_handler import SuperUserHandler
from ..schemas.user_schemas import (
    ResponseUserSchema, CreateUserSchema, UpdateUserSchema, PaginationSchema
)


@api_controller('superuser', tags=['SuperUser'])
class SuperUserController:
    def __init__(self):
        self.handler_class = SuperUserHandler
        self.base_controller = BaseUserController(self.handler_class)
        
    @route.get('/get_users', response=list[ResponseUserSchema], auth=JWTAuth())
    def get_users(self, query: Query[PaginationSchema]):
        self.handler = self.handler_class()
        return (self.handler.get_users(query))
    
    @route.post(
        '/create_superuser', response=ResponseUserSchema, auth=JWTAuth()
    ) 
    def create_superuser(self, user_in: CreateUserSchema):
        return self.base_controller.create_user(user_in)
    
    @route.put('/update_superuser', response=ResponseUserSchema, auth=JWTAuth())
    def update_superuser(self, request: HttpRequest, user_in: UpdateUserSchema):
        return self.base_controller.update_user(request, user_in)
    
    @route.put(
        'change_superuser_password', response=ResponseUserSchema, auth=JWTAuth()
    )
    def change_superuser_password(self, request: HttpRequest, newpassword: str):
        return self.base_controller.change_user_password(request, newpassword)
    
    @route.delete(
        '/deactivate_superuser/', response=ResponseUserSchema, auth=JWTAuth()
    )
    def deactivate_superuser(self, request: HttpRequest, username):
        request.username = username
        return self.base_controller.deactivate_user(request)
        