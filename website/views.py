from flask.helpers import url_for
from . import db, log
from website.models import Post, User

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    log.debug("Received a GET request at `/home`")
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


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
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    """Allows the user to delete a post"""
    post = Post.query.filter_by(id=id).first()

    # check whether the post exists
    if not post:
        flash("Post does not exists.", category="error")

    # check whether the current user ID is same as the post ID
    elif current_user.id != post.id:
        flash("You do not have permission to delete this post", category="error")

    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    # check whether the username exists
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No user with that username exists", category="error")
        return redirect(url_for("views.home"))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=username, posts=posts)
