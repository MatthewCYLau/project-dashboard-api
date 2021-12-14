class Project:
    def __init__(self, name):
        self.name = name

    def to_dictionary(self):
        return {"name": self.name}
