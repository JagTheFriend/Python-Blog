from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint("auth", __name__)


@auth.route("/login")
def home():
    return render_template("login.html")


@auth.route("/sign-up")
def sign_up():
    return render_template("signup.html")


@auth.route("/logout")
def login():
    """Redirects the user to the home page
    when the user clicks on the logout button
    """
    return redirect(url_for("views.home"))
