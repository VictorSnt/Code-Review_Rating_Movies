from ninja_extra import api_controller, route
from ..services.user_handler import UserHandler
from ..schemas.user_schemas import (
    ResponseUserSchema, CreateUserSchema, UpdateUserSchema
)

@api_controller('user', tags=['User'])
class UserController:

    @route.get('/get', response=ResponseUserSchema)
    def get_user(self, username: str):
        handler = UserHandler()
        response = handler.get_user(pk=username)
        return response
    
    @route.post('/create', response=ResponseUserSchema) 
    def create(self, user_in: CreateUserSchema):
        handler = UserHandler()
        response = handler.create_user(user_schema=user_in)
        return response
    
    @route.put('/update', response=ResponseUserSchema)
    def update(self, username: str, user_in: UpdateUserSchema):
        handler = UserHandler()
        response = handler.update_user(pk=username, user_schema=user_in)
        return response

    @route.put('changepassword', response=ResponseUserSchema)
    def change_password(self, username: str, newpassword: str):
        handler = UserHandler()
        response = handler.change_password(
            pk=username, newpassword=newpassword
        )
        return response
    
    @route.delete('/delete', response=ResponseUserSchema)
    def delete(self, username: str):
        handler = UserHandler()
        response = handler.inativate_user(pk=username)
        return response
    