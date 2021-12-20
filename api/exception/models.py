from flask import jsonify


class UnauthorizedException(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def generate_exception_response(self):
        res = dict()
        res["errors"] = [{"message": self.message}]
        return jsonify(res), self.status_code


class BadRequestException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def generate_exception_response(self):
        res = dict()
        res["errors"] = [{"message": self.message}]
        return jsonify(res), self.status_code
