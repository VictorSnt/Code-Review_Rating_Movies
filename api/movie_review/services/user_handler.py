from django.contrib.auth.models import User
from ninja.errors import HttpError
from ..schemas.user_schemas import CreateUserSchema, UpdateUserSchema


class UserHandler:
    def __init__(self, request=None) -> None:
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
        return user
    
    def inativate_user(self) -> User:
        user = self.user
        user.is_active = False
        user.save()
        return user
    
class SuperUserHandler(UserHandler):

    def get_users(self, paginated, page, page_size) -> list[User]: 
        if paginated:
            start = (page - 1) * page_size
            end = start + page_size
            users = User.objects.filter(
                is_active=True, is_superuser=False
                )[start:end]
        else:    
            users = User.objects.all()
        if not users.exists():
            raise HttpError(404, "Nenhum usuario encontrado")
        return users.order_by('username')
    
    def create_user(self, user_schema: CreateUserSchema):
        user_dict = user_schema.remove_null_fields()
        user = User.objects.create_user(**user_dict)
        user.is_superuser = True
        user.save()
        return user
    
    def inativate_user(self, pk=None) -> User:
        if not pk:
            user = self.user
        else:
            user = User.objects.get(username=pk)
        user.is_active = False
        user.save()
        return user