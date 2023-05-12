from my_flask_api.auth import auth
from flask_restful import Resource


class PrivateAbstractView(Resource):
    decorators = [auth.login_required]


class PublicAbstractView(Resource):
    pass
