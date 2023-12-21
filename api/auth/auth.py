from flask import request
from api.db.setup import db
from api.exception.models import UnauthorizedException
import os
import jwt
import logging
from functools import wraps


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if "x-auth-token" in request.headers:
            token = request.headers["x-auth-token"]

        if not token:
            raise UnauthorizedException("Token missing", status_code=401)

        try:
            data = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms="HS256")
            user = db["users"].find_one({"email": data["email"]}, {"password": False})
        except Exception as e:
            logging.error(e)
            raise UnauthorizedException("Invalid token", status_code=401)

        return f(user, *args, **kwargs)

    return decorator
