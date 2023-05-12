from my_flask_api.daos.user_dao import UserDao
from my_flask_api.config import FLASK_SECRET_KEY


from flask_httpauth import HTTPTokenAuth
import jwt

auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token, FLASK_SECRET_KEY, algorithms=["HS256"])
        email = data["email"]
        user = UserDao.get_user(email)
        if user:
            return user
    except Exception as e:
        raise e
