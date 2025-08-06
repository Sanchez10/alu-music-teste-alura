from flask_login import UserMixin

class UserFake(UserMixin):
    def __init__(self, id):
        self.id = id
        