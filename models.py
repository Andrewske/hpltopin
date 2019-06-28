from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    pinterest_username = db.Column(db.String(100), unique=True, nullable=True)
    profile_url = db.Column(db.String(100), nullable=True)
    profile_pic = db.Column(db.String(100), nullable=False, default="default.jpg")
    access_token = db.Column(db.String(1000), nullable=True)
    boards = db.relationship("Board", backref="user", lazy=True)
    pins = db.relationship("Pin", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"


class Board(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=True)
    board_name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    url = db.Column(db.String(100), nullable=False)
    pins = db.relationship("Pin", backref="username", lazy=True)

    def __repr__(self):
        return f"Board('{self.username}', '{self.board_name}')"


class Pin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Board('{self.username}', '{self.board_name}')"


if __name__ == "__main__":
    pass
