from ninja_jwt.controller import NinjaJWTDefaultController
from .controllers.superuser_controller import SuperUserController
from .controllers.user_controller import UserController
from .controllers.movies_controller import MoviesController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(SuperUserController)
api.register_controllers(UserController)
api.register_controllers(MoviesController)
api.register_controllers(NinjaJWTDefaultController)



