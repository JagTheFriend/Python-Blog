from flask.helpers import url_for
from . import db, log
from website.models import Comment, Like, Post, User

from flask import Blueprint, render_template, request, flash, redirect, jsonify
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

    posts = user.posts
    return render_template("posts.html", user=username, posts=posts)


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    """Allows the user to comment on a post"""
    text = request.form.get("text")
    if not text:
        flash("Comment cannot be empty", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            # create a new comment
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added", category="success")
        else:
            flash("Post does not exist", category="error")
    return redirect(url_for("views.home"))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        # delete the comment
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/like-post/<post_id>", methods=["POST"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)

    # unlike the post of the user has already liked the post
    elif like:
        db.session.delete(like)
        db.session.commit()

    # like the post if the user hasn't already liked the post
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({
        "likes": len(post.likes),
        "liked": current_user.id in map(lambda x: x.author, post.likes)
    }
    )
