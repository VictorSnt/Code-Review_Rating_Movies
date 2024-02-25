from ninja_extra import api_controller, route
from ..services.user_handler import UserHandler
from ..schemas.user_schemas import (
    UserSchema, UpdateUserSchema, 
)
from django.contrib.auth.models import User


@api_controller('user', tags=['User'])
class UserController:

    @route.post('/create', response=UserSchema) 
    def create(self, user_in: UserSchema):
        handler = UserHandler()
        response = handler.create_user(user_schema=user_in)
        return response
    
    @route.put('/update', response=UserSchema)
    def update(self, username: str, user_in: UpdateUserSchema):
        handler = UserHandler()
        response = handler.update_user(pk=username, user_schema=user_in)
        return response
        
    @route.delete('/delete', response=UserSchema)
    def delete(self, username: str):
        handler = UserHandler()
        response = handler.inativate_user(pk=username)
        return response
    
    @route.get('/get', response=UserSchema)
    def get_user(self, username: str):
        handler = UserHandler()
        response = handler.get_user(pk=username)
        return response

    @route.put('changepassword', response=UserSchema)
    def change_password(self, username: str, newpassword: str):
        handler = UserHandler()
        response = handler.change_password(
            pk=username, newpassword=newpassword
        )
        return response
