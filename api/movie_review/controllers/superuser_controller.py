from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller, route
from ..controllers.baseuser_controller import BaseUserController
from ..services.superuser_handler import SuperUserHandler
from ..schemas.user_schemas import (
    ResponseUserSchema, CreateUserSchema, UpdateUserSchema
)


@api_controller('superuser', tags=['SuperUser'])
class SuperUserController(BaseUserController):
    handler_class = SuperUserHandler
    
    @route.get('/get_users', response=list[ResponseUserSchema], auth=JWTAuth())
    def get_users(self, paginated=False, page=1, page_size=10):
        self.handler = self.handler_class()
        response = self.handler.get_users(paginated, page, page_size)
        return response
    
    @route.post('/create', response=ResponseUserSchema, auth=JWTAuth()) 
    def create_superuser(self, user_in: CreateUserSchema):
        super().create(user_in)
    
    @route.put('/update', response=ResponseUserSchema, auth=JWTAuth())
    def update_superuser(self, request: HttpRequest, user_in: UpdateUserSchema):
        super().update(request, user_in)
    
    @route.put('changepassword', response=ResponseUserSchema, auth=JWTAuth())
    def change_superuser_password(self, request: HttpRequest, newpassword: str):
        super().change_password(request, newpassword)
    
    @route.delete('/deactivate', response=ResponseUserSchema, auth=JWTAuth())
    def inativate_superuser(self, request: HttpRequest, pk=None):
        self.handler = self.handler_class(request)
        response = self.handler.inativate_user(pk=pk)
        return response
    