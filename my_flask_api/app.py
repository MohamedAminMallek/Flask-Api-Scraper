from flask import Flask
from flask_restful import Api
from flask import abort
from webargs.flaskparser import parser
from flask_cors import CORS
from my_flask_api.config import FLASK_SECRET_KEY


app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
api = Api(app, prefix="/my-flask-api/v1")
CORS(app)


@parser.error_handler
def handle_parse_error(error, req, schema, *, error_status_code, error_headers):
    abort(422, error.messages)
