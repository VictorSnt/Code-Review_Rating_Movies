from django.contrib.auth.models import User
from ninja.errors import HttpError
from ..schemas.user_schemas import CreateUserSchema
from .user_handler import UserHandler

class SuperUserHandler(UserHandler):
    def __init__(self, request=None) -> None:
        super().__init__(request)
        if not self.user or not self.user.is_superuser:
            HttpError(400, "Precisa ser superusuario")
        
    def get_users(self, paginated, page, page_size) -> list[User]: 
        if paginated:
            start = (page - 1) * page_size
            end = start + page_size
            users = User.objects.filter(
                is_active=True, is_superuser=False
                ).order_by('username')[start:end]
        else:    
            users = User.objects.filter(
                is_active=True, is_superuser=False
            ).order_by('username')
        if not users.exists():
            raise HttpError(404, "Nenhum usuario encontrado")
        return users
    
    def create_user(self, user_schema: CreateUserSchema):
        user_dict = user_schema.remove_null_fields()
        user = User.objects.create_user(**user_dict)
        user.is_superuser = True
        user.save()
        return user
    
    
    