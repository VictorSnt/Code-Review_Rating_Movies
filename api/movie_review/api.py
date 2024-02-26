from ninja_jwt.controller import NinjaJWTDefaultController
from .controllers.user_controller import UserController
from .controllers.superuser_controller import SuperUserController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(UserController)
api.register_controllers(SuperUserController)
api.register_controllers(NinjaJWTDefaultController)



