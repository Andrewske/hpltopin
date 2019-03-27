from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from db import DatabaseConnection
from bs4 import BeautifulSoup
from flask_login import LoginManager
import pinterest, bonanza, giphy, templates
import urllib, json
from urllib.request import urlopen
import secrets
from class_pinterest import Pinterest


gifs = ["https://media.giphy.com/media/nXxOjZrbnbRxS/giphy.gif"]

authentication_url = "https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https%3A%2F%2Fwww.hpltopin.com%2Fsuccess&client_id=5021381484636841344&scope=%5B%27read_public%27%2C+%27write_public%27%5D"

# Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221


app = Flask(__name__)
app.secret_key = secrets.secret_key

db = DatabaseConnection()
login_manager = LoginManager()
login_manager.init_app(app)
p = Pinterest()


@app.route("/", methods=["GET", "POST"])
def index():
    code = request.args.get("code", None)
    if code == None:
        return render_template("index.html")
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
            return templates.no_success(access_token_error)


@app.route("/authenticate_user", methods=["GET", "POST"])
def get_access_token():
    return redirect(secrets.test_auth_url)


@app.route("/success", methods=["GET", "POST"])
def create_and_post():
    hpl_url = request.form.get("hpl_url")
    if hpl_url == None:
        return render_template(
            "no_success.html",
            error="hpl_url: " + hpl_url,
            no_success_gif=giphy.get_gif("uh oh"),
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
                return templates.no_success(data[0])
            else:
                success_gif = giphy.get_gif("success")
                return render_template(
                    "success.html",
                    data=data,
                    title=title,
                    board_url=board_url,
                    success_gif=success_gif,
                )
        else:
            return templates.no_success(board_url)


@app.route("/test", methods=["GET", "POST"])
def test():
    bonanza.set_hpl(request.form["hpl_url"])
    return redirect(url_for("test2"))


@app.route("/test2", methods=["GET", "POST"])
def test2():
    username = "kevinbigfoot"
    access_token = "super_new_access_token"
    db.create_user(username, access_token)
    return render_template(
        "no_success.html", error=username, no_success_gif=giphy.get_gif("uh oh")
    )

    # hpl_url = 'https://www.bonanza.com/hpl/Favorite-Comic-Book-Superheroes/163721'
    # access_token = secrets.pinterest_test_key
    # if isinstance(access_token, str):
    #     if hpl_url == None:
    #         return render_template(
    #             "no_success.html",
    #             error="No HPL U",
    #             no_success_gif=giphy.get_gif("uh oh"),
    #         )
    #     else:
    #         listings, title = bonanza.find_listings(hpl_url)
    #         listings_info = bonanza.get_items_information(listings)
    #         try:
    #             username = pinterest.get_username(access_token)
    #         except:
    #             return render_template(
    #                 "no_success.html",
    #                 error="Couldn't Get Username",
    #                 no_success_gif=giphy.get_gif("uh oh"),
    #             )
    #         else:
    #             board_url = (
    #                 "https//www.pinterest.com/kevinbigfoot/test"
    #             )  # pinterest.create_pinterest_board(title, username, access_token)
    #             if "www" not in board_url:
    #                 return render_template(
    #                     "no_success.html",
    #                     error=board_url,
    #                     no_success_gif=giphy.get_gif("uh oh"),
    #                 )
    #             else:
    #                 data = []
    #                 for listing in listings_info:
    #                     data.append(
    #                         pinterest.post_item_to_pinterest(
    #                             listing, title, username, access_token
    #                         )
    #                     )
    #                 if "message" in data[0]:
    #                     return render_template(
    #                         "no_success.html",
    #                         error=data[0],
    #                         no_success_gif=giphy.get_gif("uh oh"),
    #                     )
    #                 else:
    #                     success_gif = giphy.get_gif("success")
    #                     return render_template(
    #                         "success.html",
    #                         data=data,
    #                         title=title,
    #                         board_url=board_url,
    #                         success_gif=success_gif,
    #                     )
    # else:
    #     return render_template(
    #         "no_success.html", error=access_token, no_success_gif=giphy.get_gif("uh oh")
    #     )


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(user_id)
    except:
        return None


@app.errorhandler(404)
def pageNotFound(e):
    return (
        render_template(
            "no_success.html",
            error="Page Not Found",
            no_success_gif=giphy.get_gif("uh oh"),
        ),
        404,
    )


@app.errorhandler(500)
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

