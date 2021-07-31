from . import db, log
from website.models import Post

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    log.debug("Received a GET request at `/home`")
    return render_template("home.html", user=current_user)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:  # there is no text
            flash("Post cannot be empty", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            log.info("Created post")
            flash("Post created!", category="success")

    return render_template("create_post.html", user=current_user)
