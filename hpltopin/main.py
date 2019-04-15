from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
)
from hpltopin import db
from .models import User, Board, Pin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_required, current_user
from hpltopin import bonanza, site_templates as t
import urllib, json
from urllib.request import urlopen
import secrets
from hpltopin.class_pinterest import Pinterest
from hpltopin.giphy import get_gif


gifs = ["https://media.giphy.com/media/nXxOjZrbnbRxS/giphy.gif"]


# Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221


main = Blueprint("main", __name__)

p = Pinterest()


@main.route("/", methods=["GET", "POST"])
def index():
    user = current_user
    if user.is_authenticated:
        return render_template("user_homepage.html", welcome_gif=get_gif("hi friend"))
    else:
        return render_template("anon_homepage.html", welcome_gif=get_gif("hi"))


@main.route("/profile")
@login_required
def profile():
    user = current_user
    # if user.access_token and not user.pinterest_username:
    #     try:
    #         user.pinterest_username = p.set_username(access_token=user.access_token)
    #         db.session.add(user)
    #         db.session.commit()
    #         return t.profile()
    #     except:
    #         return t.profile(message="exception")
    # else:
    return t.profile()


@main.route("/authenticate_user", methods=["GET", "POST"])
@login_required
def get_access_token():
    code = request.args.get("code", None)
    if code == None:
        return render_template("profile.html", welcome_gif=get_gif("hi"))
    else:
        if current_user.is_authenticated:
            user = current_user
            user.access_token = p.get_access_token(code)
            try:
                db.session.add(user)
                db.session.commit()
                return t.profile(
                    username=current_user.username, access_token=user.access_token
                )
            except:
                return t.profile(message="didn't save access token")
        else:
            return t.no_success(error="No current user")


@main.route("/pin_list", methods=["GET", "POST"])
@login_required
def pin_list():
    user = current_user
    if request.method == "POST":
        hpl_url = request.form.get("hpl_url")
        listings, title = bonanza.find_listings(hpl_url)
        session["title"] = title
        session["listings_info"] = bonanza.get_items_information(listings)
        return t.pin_list(
            username=user.username,
            listing_count=len(listings),
            board_name=title,
            hpl_url=hpl_url,
        )
    else:
        return t.pin_list(username=user.username)


@main.route("/create_and_post", methods=["GET", "POST"])
def create_and_post():
    user = current_user
    title = session.get("title", None)
    listings_info = session.get("listings_info", None)
    board_url = p.create_pinterest_board(title=title)
    if isinstance(board_url, str):
        data = []
        for listing in listings_info:
            data.append(p.post_item_to_pinterest(listing, title))
        if "message" in data[0]:
            return t.no_success(data[0])
        else:
            return t.success(data=data, title=title, board_url=board_url)
    else:
        return t.no_success(error=board_url)


@main.route("/test", methods=["GET", "POST"])
def test():
    bonanza.set_hpl(request.form["hpl_url"])
    return redirect(url_for("test2"))


@main.errorhandler(404)
def pageNotFound(e):
    return (t.no_success(error="Page not Found"), 404)


@main.errorhandler(500)
def serviceError(e):
    return (t.no_success(error="Internal Service Error"), 500)


if __name__ == "__main__":
    context = ("example.com+5.pem", "example.com+5-key.pem")
    app.run(debug=True, ssl_context=context)

