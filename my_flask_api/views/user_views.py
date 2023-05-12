from my_flask_api.views.abstract_views import PublicAbstractView, PrivateAbstractView
from webargs.flaskparser import use_kwargs
from marshmallow import Schema
from webargs import fields
from my_flask_api.daos.user_dao import UserDao, generate_auth_token
from google.oauth2 import id_token
import google.auth


class UserSchema(Schema):
    class Meta:
        strict = True

    name = fields.Str(required=True, location="view_args")
    email = fields.Str(required=True, location="view_args")
    password = fields.Str(required=True, location="view_args")


class OauthLoginSchema(Schema):
    class Meta:
        strict = True

    token = fields.Str(required=True, location="view_args")


class UserView(PublicAbstractView):
    @use_kwargs(UserSchema)
    def post(self, name, email, password):
        user = UserDao.add_user(name, email, password, generate_auth_token(email))
        return {"data": user}, 201


class UserGoogleLogin(PublicAbstractView):
    @use_kwargs(OauthLoginSchema)
    def post(self, token):
        request = google.auth.transport.requests.Request()

        try:
            decoded_token = id_token.verify_token(token, request)
            email = decoded_token["email"]
            user = UserDao.get_user(email)
            if not user:
                user = UserDao.add_user(decoded_token["name"], email, "1234", None)
            user.token = generate_auth_token(email)
        except ValueError:
            # Verification failed.
            return {"message": "Invalid token"}, 400

        return {
            "name": user.name,
            "email": user.email,
            "token": user.token,
            "image": decoded_token["picture"],
        }, 200


class UsersView(PrivateAbstractView):
    def get(self):
        return [
            {
                "name": user.name,
                "email": user.email,
                "token": user.token,
            }
            for user in UserDao.get_all_users()
        ], 200
