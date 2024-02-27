from django.contrib.auth import get_user_model
from ninja.errors import HttpError
from ..schemas.user_schemas import CreateUserSchema, PaginationSchema
from .user_handler import UserHandler

User = get_user_model()

class SuperUserHandler(UserHandler):
    def __init__(self, request=None) -> None:
        super().__init__(request)
        if not self.user or not self.user.is_superuser:
            HttpError(400, "Precisa ser superusuario")
        
    def get_users(self, query: PaginationSchema) -> list: 
        
        if query.paginated:
            start = (query.page - 1) * query.page_size
            end = start + query.page_size
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
        user = User.objects.create_superuser(**user_dict)
        return user
    
    def inativate_user(self):
        try:
            if self.request.user.is_superuser:
                username = self.request.username
                user = User.objects.get(username=username)
                user.is_active = False
                user.save()
                return user
            else:
                raise HttpError(400, 'Você precisa ser superuser')
        except User.DoesNotExist:
                raise HttpError(400, "Usuario não encontrado")
            
        
    
    