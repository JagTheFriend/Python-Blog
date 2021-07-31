from re import findall

from . import log, db
from flask.helpers import flash
from .models import User

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        log.debug("Received a POST request on `/login`")

        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                log.info("Logged in")
                flash("Logged in!", category="success")
                login_user(remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email does not exists.", category="error")

    log.debug("Received GET request on `/login`")
    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        log.debug("Received a 'POST' request on `/sign-up`")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password1")
        password1 = request.form.get("password2")
        log.debug(f"Email: {email!r}, Password: {password!r}, Repeat password: {password1!r}")
        # check whether the email has a valid form
        if not findall(EMAIL_REGEX, email):
            flash("Invalid Email!", category="error")

        # check whether email exists
        elif User.query.filter_by(email=email).first():
            flash("Email is already in use.", category="error")

        # check whether usename exists
        elif User.query.filter_by(username=username).first():
            flash("Username is already in use.", category="error")

        # the passwords don't match
        elif password1 != password:
            flash("Passwords don't match", category="error")

        # check whether the username is too short
        elif len(username) < 1:
            flash("Username is too short", category="error")

        # check whether the password is too short
        elif len(password) < 6:
            flash("Password is too short", category="error")

        else:
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()

            log.debug("Created new user")
            login_user(new_user, remember=True)
            flash("User Created!")
            # redirect the user to the home page
            return redirect(url_for("views.home"))

    # TODO: Add a way to verify the email
    log.debug("Received GET request on `/signup`")
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required  # You can only access this page if you have logged in
def logout():
    """Redirects the user to the home page
    when the user clicks on the logout button
    """
    return redirect(url_for("views.home"))
