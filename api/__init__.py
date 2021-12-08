from dotenv import load_dotenv
from flask import Flask
from .db.setup import db_connect
from api.auth import views as auth

load_dotenv("config/.env")


app = Flask(__name__)
app.register_blueprint(auth.bp)

db_connect()


@app.route("/ping")
def ping():

    return "pong!"
