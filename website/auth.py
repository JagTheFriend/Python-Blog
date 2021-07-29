from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login")
def home():
    return "<h1>Login</h1>"


@auth.route("/sign-up")
def sign_up():
    return "<h1>sign-up</h1>"


@auth.route("/logout")
def login():
    return "<h1>logout</h1>"
