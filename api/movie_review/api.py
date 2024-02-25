from ninja_jwt.controller import NinjaJWTDefaultController
from .controllers.user_controller import UserController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(UserController)
