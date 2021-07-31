from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    # unique ID of the user
    id = db.Column(db.Integer, primary_key=True)
    # max length of 150 characters, and it must be unique
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)  # username
    password = db.Column(db.String(150))  # doesn't need to be unique
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship("Post", backref="user", passive_deletes=True)


class Post(db.Model):
    # unique ID of the post
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)  # can't be empty
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # when the user deletes the account, delete all the posts made by that user
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
