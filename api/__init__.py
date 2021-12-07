from dotenv import load_dotenv
from flask import Flask
from .db.setup import db_connect

load_dotenv("config/.env")


app = Flask(__name__)

db_connect()


@app.route("/ping")
def ping():

    return "pong!"
