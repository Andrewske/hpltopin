from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    access_token = db.Column(db.String(100), nullable=True)

    def __init__(self, username, password, access_token):
        self.username = username
        self.password = password
        self.access_token = access_token

    def __repr__(self):
        return "<User %r>" % self.username


if __name__ == "__main__":
    pass
