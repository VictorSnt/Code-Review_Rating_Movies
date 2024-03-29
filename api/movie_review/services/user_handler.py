from django.contrib.auth.models import User
from ..schemas.user_schemas import CreateUserSchema, UpdateUserSchema
from ninja.errors import HttpError
class UserHandler:
    def __init__(self, request=None) -> None:
        self.request = request
        self.user: User = request.user if request else None
   
    
    def create_user(self, user_schema: CreateUserSchema):
        user_dict = user_schema.remove_null_fields()
        user = User.objects.create_user(**user_dict)
        return user
    
    def update_user(self, user_schema: UpdateUserSchema) -> User:
        update_data = user_schema.remove_null_fields()
        user = self.user
        for field, value in update_data.items():
            setattr(user, field, value)
        user.save()
        return user

    def change_password(self, newpassword):
        user = self.user
        user.set_password(newpassword)
        user.save()
        if not user.check_password(newpassword):
            raise HttpError(400, 'Erro ao alterar senha')
        return user
    
    def deactivate_user(self) -> User:
        user = self.user
        user.is_active = False
        user.save()
        return user
    
