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
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from . import pinterest, bonanza, site_templates as t
import urllib, json
from urllib.request import urlopen
import secrets
from .class_pinterest import Pinterest
from .giphy import get_gif


gifs = ["https://media.giphy.com/media/nXxOjZrbnbRxS/giphy.gif"]

authentication_url = "https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https%3A%2F%2Fwww.hpltopin.com%2Fsuccess&client_id=5021381484636841344&scope=%5B%27read_public%27%2C+%27write_public%27%5D"

# Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221


main = Blueprint("main", __name__)

p = Pinterest()


@main.route("/", methods=["GET", "POST"])
def index():
    code = request.args.get("code", None)
    if code == None:
        return render_template("index.html", welcome_gif=get_gif("hi"))
    else:
        access_token_error = p.get_access_token(code)
        if isinstance(p.access_token, str):
            response = p.set_username()
            return render_template(
                "authenticated.html",
                username=p.username,
                response=response,
                access_token=p.access_token,
            )
        else:
            return t.no_success(access_token_error)


@main.route("/profile")
@login_required
def profile():
    return render_template(
        "profile.html",
        profile_gif=get_gif("you made it"),
        username=current_user.username,
        auth_url=p.get_auth_url(),
    )


@main.route("/authenticate_user", methods=["GET", "POST"])
def get_access_token():
    code = request.args.get("code", None)
    if code == None:
        return render_template("index.html", welcome_gif=get_gif("hi"))
    else:
        if current_user.is_authenticated:
            user = current_user
            user.access_token = p.get_access_token(code)
            return render_template(
                "pin_list.html",
                username=current_user.username,
                access_token=user.access_token,
            )
        else:
            return t.no_success(error="No current user")


@main.route("/success", methods=["GET", "POST"])
def create_and_post():
    hpl_url = request.form.get("hpl_url")
    if hpl_url == None:
        return render_template(
            "no_success.html",
            error="hpl_url: " + hpl_url,
            no_success_gif=get_gif("uh oh"),
        )
    else:
        listings, title = bonanza.find_listings(hpl_url)
        listings_info = bonanza.get_items_information(listings)
        board_url = pinterest.create_pinterest_board(title)
        if isinstance(board_url, str):
            data = []
            for listing in listings_info:
                data.append(pinterest.post_item_to_pinterest(listing, title))
            if "message" in data[0]:
                return t.no_success(data[0])
            else:
                success_gif = get_gif("success")
                return render_template(
                    "success.html",
                    data=data,
                    title=title,
                    board_url=board_url,
                    success_gif=success_gif,
                )
        else:
            return t.no_success(board_url)


@main.route("/test", methods=["GET", "POST"])
def test():
    bonanza.set_hpl(request.form["hpl_url"])
    return redirect(url_for("test2"))


@main.route("/test2", methods=["GET", "POST"])
def test2():
    username = "kevinbigfoot"
    access_token = "super_new_access_token"
    db.create_user(username, access_token)
    return render_template(
        "no_success.html", error=username, no_success_gif=get_gif("uh oh")
    )


@main.errorhandler(404)
def pageNotFound(e):
    return (
        render_template(
            "no_success.html",
            error="Page Not Found",
            no_success_gif=giphy.get_gif("uh oh"),
        ),
        404,
    )


@main.errorhandler(500)
def serviceError(e):
    return (
        render_template(
            "no_success.html",
            error="Internal Service Error",
            no_success_gif=giphy.get_gif("uh oh"),
        ),
        500,
    )


if __name__ == "__main__":
    context = ("example.com+5.pem", "example.com+5-key.pem")
    app.run(debug=True, ssl_context=context)

