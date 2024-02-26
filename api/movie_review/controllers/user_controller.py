from ninja_extra import api_controller
from ..services.user_handler import UserHandler
from ..controllers.baseuser_controller import BaseUserController


@api_controller('user', tags=['User'])
class UserController(BaseUserController):
    handler_class = UserHandler
