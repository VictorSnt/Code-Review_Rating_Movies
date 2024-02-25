from django.contrib.auth.models import User
from ninja.errors import HttpError
from ..schemas.user_schemas import UpdateUserSchema, UserSchema


class UserHandler:
    def get_user(self, pk) -> User:
        user = User.objects.filter(username=pk).first()
        if not user:
            raise HttpError(404, "Objeto não encontrado")
        return user
    
    def create_user(self, user_schema: UserSchema):
        user_dict = user_schema.model_dump()
        user = User.objects.create_user(**user_dict)
        return user
    
    def update_user(self, pk: str, user_schema: UpdateUserSchema) -> User:
        is_updated = False
        update_data = user_schema.model_dump()
        user = self.get_user(pk)
        for field, value in update_data.items():
            if value:
                setattr(user, field, value)
                is_updated = True
        if not is_updated:
            raise HttpError(400, "Nenhum campo valido foi preenchido") 
        else:
            user.save()
            return user

    def inativate_user(self, pk: str) -> User:
        user = self.get_user(pk=pk)
        user.is_active = False
        user.save()
        return user
    
    def change_password(self, pk, newpassword):
        user = self.get_user(pk=pk)
        user.set_password(newpassword)
        user.save()
        return user