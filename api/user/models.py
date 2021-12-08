class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_dictionary(self):
        return {"email": self.email, "password": self.password}
