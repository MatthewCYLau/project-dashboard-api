import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .db.setup import db_connect
from api.user import views as user
from api.project import views as project
from api.skill import views as skill
from api.comment import views as comment
from api.like import views as like
from api.exception.models import *
from api.data.setup import generate_placeholder_data

load_dotenv("config/.env")


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(user.bp, url_prefix="/api")
app.register_blueprint(project.bp, url_prefix="/api")
app.register_blueprint(skill.bp, url_prefix="/api")
app.register_blueprint(comment.bp, url_prefix="/api")
app.register_blueprint(like.bp, url_prefix="/api")

logging.basicConfig(level=logging.INFO)


@app.errorhandler(UnauthorizedException)
@app.errorhandler(BadRequestException)
def handle_unauthorized_exception(e):
    return e.generate_exception_response()


if os.environ.get("MONGO_DB_CONNECTION_STRING"):
    db_connect()
    generate_placeholder_data()


@app.route("/ping")
def ping():
    return "pong!"
