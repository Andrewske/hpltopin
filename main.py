from flask import Flask, render_template, request, jsonify, redirect
import pinterest, bonanza, giphy
import urllib
import secrets


SECRET_KEY = "development key"

gifs = ["https://media.giphy.com/media/nXxOjZrbnbRxS/giphy.gif"]

authentication_url = "https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https%3A%2F%2Fwww.hpltopin.com%2Fsuccess&client_id=5021381484636841344&scope=%5B%27read_public%27%2C+%27write_public%27%5D"

# Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/authenticate_user", methods=["GET", "POST"])
def authenticate_user():
    if request.method == "POST":
        bonanza.set_hpl(request.form["hpl_url"])
        auth_url = pinterest.authenticate_user()
        return redirect(auth_url)
    else:
        return render_template("index.html")


@app.route("/success", methods=["GET", "POST"])
#This page is reached after the user verifys with Pinterest. The URL conains the authorization_code. 
def create_and_post():
    #Using the code from the URL, get the access token. If it worked then the access token will be a string. 
    access_token = secrets.pinterest_test_key #pinterest.get_access_token(request.args.get("code"))
    #If the access token is a string we will procede
    if isinstance(access_token, str):
        #This will throw a type error if there is no hpl_url. 
        if bonanza.hpl_url == None:
            return render_template("no_success.html", error="No HPL U", no_success_gif=giphy.get_gif("uh oh"))  
        else: 
            #find listings, title, and info from Bonanza
            listings, title = bonanza.find_listings(bonanza.hpl_url)
            listings_info = bonanza.get_items_information(listings)
            #Create a pinterest board
            board_url = pinterest.create_pinterest_board(title, access_token)
            if "exceeded" in board_url:
                return render_template("no_success.html", error=board_url, no_success_gif=giphy.get_gif("uh oh"))
            else:
                data = []
                try: 
                    for listing in listings_info:
                        data.append(
                            pinterest.post_item_to_pinterest(listing, username, title, access_token)
                        ) 
                except:
                    print("Not listing correctly")
                else:
                    success_gif = giphy.get_gif("success")
                    return render_template(
                        "success.html",
                        data=data,
                        username=username,
                        title=title,
                        board_url=board_url,
                        success_gif=success_gif,
                    )
    else:
        return render_template("no_success.html", error=access_token, no_success_gif=giphy.get_gif("uh oh"))


@app.route("/test", methods=["GET", "POST"])
def test():
    data = [
        "https://www.pinterest.com/pin/144678206765760738/",
        "https://www.pinterest.com/pin/144678206765760739/",
    ]
    username = "BonanzaMarket"
    title = "test"
    board_url = "https://www.bonanza.com/hpl/Garden-Tools/163708"

    error = None
    access_token = secrets.pinterest_test_key
    
    if not isinstance(access_token, str):
        return render_template(
            "no_success.html", error=error, no_success_gif=giphy.get_gif("uh oh"))  
    else:
        username = pinterest.get_username(access_token)
        hpl_url = 'https://www.bonanza.com/hpl/Shades-and-Sunnies/163720'
        listings, title = bonanza.find_listings(hpl_url)
        listings_info = bonanza.get_items_information(listings)
        board_url = pinterest.create_pinterest_board(title, access_token)
        for listing in listings_info:
            try: 
                data.append(
                    pinterest.post_item_to_pinterest(listing, username, title, access_token)
                )
            except:
                return render_template("no_success.html", error=error, no_success_gif=giphy.get_gif("uh oh"))
    if error == None:
        success_gif = giphy.get_gif("success")
        return render_template(
            "success.html",
            data=data,
            username=username,
            title=title,
            board_url=board_url,
            success_gif=success_gif,
        )
    else:
        return render_template(
            "no_success.html", error=error, no_success_gif=giphy.get_gif("uh oh"))

@app.errorhandler(404)
def pageNotFound(e):
    return render_template(
            "no_success.html", error='Page Not Found', no_success_gif=giphy.get_gif("uh oh")), 404

@app.errorhandler(500)
def pageNotFound(e):
    return render_template(
            "no_success.html", error='Internal Service Error', no_success_gif=giphy.get_gif("uh oh")), 500


if __name__ == "__main__":
    app.run(debug=True)


# 1. User enters the URL for the HPL
# 2. We send them to the Pinterest Authentication
# 3. Pinterest returns them to the redirect url with an access token
# Example: https://andrewske.github.io/pinterest-bonanza-api/?state=768uyFys&code=f3bb9c23
