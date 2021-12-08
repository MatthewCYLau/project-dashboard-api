from dotenv import load_dotenv
from flask import Flask
from .db.setup import db_connect
from api.user import views as user

load_dotenv("config/.env")


app = Flask(__name__)
app.register_blueprint(user.bp, url_prefix="/api")

db_connect()


@app.route("/ping")
def ping():

    return "pong!"
