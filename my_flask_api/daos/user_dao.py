from collections import namedtuple
from datetime import datetime, timedelta
import jwt

from werkzeug.security import generate_password_hash
from my_flask_api.config import FLASK_SECRET_KEY


def generate_auth_token(email, expires_in=60 * 60):
    expiration_date = datetime.utcnow() + timedelta(seconds=expires_in)
    return jwt.encode(
        {"email": email, "exp": expiration_date}, FLASK_SECRET_KEY, algorithm="HS256"
    )


# User = namedtuple("User", ["id", "name", "email", "password", "token"])
class User:
    def __init__(self, id, name, email, password, token):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.token = token


USERS = [
    User(
        1,
        "John",
        "John@gmail.com",
        generate_password_hash("password"),
        generate_auth_token("John@gmail.com"),
    ),
    User(
        2,
        "Susan",
        "Susan@gmail.com",
        generate_password_hash("password"),
        generate_auth_token("Susan@gmail.com"),
    ),
]


class UserDao:
    @classmethod
    def get_all_users(cls):
        return USERS

    @classmethod
    def get_user(cls, email):
        for user in cls.get_all_users():
            if user.email == email:
                return user

    @classmethod
    def add_user(cls, name, email, password, token):
        user = User(
            len(USERS) + 1, name, email, generate_password_hash(password), token
        )
        USERS.append(user)
        return user
