from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from .giphy import get_gif


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["Post"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(username=username).first()
    if request.form["action"] == "sign-up":
        if user:
            flash("Uh oh, that name it take, try again")
            return render_template("index.html", welcome_gif=get_gif("try again"))
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(username=username).first()
    elif request.form["action"] == "login":
        if not user:
            flash("Hmm... Can't find a user with that name, sign up?")
            return render_template("index.html", welcome_gif=get_gif("hmm"))
        elif not check_password_hash(user.password, password):
            flash("Ah ah ah, you didn't say the magic word")
            return render_template("index.html", welcome_gif=get_gif("ah ah ah"))
    login_user(user, remember=remember)

    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user:
        flash("Whoa someone already has that name")
        return redirect(url_for("auth.signup"))

    new_user = User(
        username=username, password=generate_password_hash(password, method="sha256")
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

