from ninja import NinjaAPI
from django_ninja_jwt.views import ObtainTokenView, RefreshTokenView


api = NinjaAPI()

@api.post('/create_user')
def create_user():
    pass

@api.put('/update_user/{id}')
def update_user(id):
    pass

@api.delete('/delete_user/{id}')
def delete_user(id):
    pass


api.add_route("/auth/jwt/create", ObtainTokenView.as_view(), methods=["POST"])
api.add_route("/auth/jwt/refresh", RefreshTokenView.as_view(), methods=["POST"])
