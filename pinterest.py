from flask import Flask, render_template
import secrets, giphy
import json
import requests


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from flask import Flask, redirect


api_url = "https://api.pinterest.com/"


def authenticate_user():
    auth_code_dict = {
        "response_type": "code",
        "redirect_uri": "https://www.hpltopin.com/success",
        "client_id": secrets.pinterest_app_id,
        "scope": "read_public, write_public, read_relationships, write_relationships",
    }
    params = urlencode(auth_code_dict, True)
    auth_url = api_url + "oauth/?" + params
    return auth_url


def get_access_token(code):
    access_token_dict = {
        "grant_type": "authorization_code",
        "client_id": secrets.pinterest_app_id,
        "client_secret": secrets.pinterest_token,
        "code": code,
    }
    response = requests.post(api_url + "v1/oauth/token", data=access_token_dict)
    response_data = json.loads(response.text)
    print(response, response_data)
    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        return response_data


def get_username(access_token):
    item_dictionary = {"access_token": access_token, "fields": "username"}
    response = requests.get(api_url + "v1/me", params=item_dictionary)
    user_data = json.loads(response.text)
    if "username" in user_data:
        return user_data["username"]
    else:
        return user_data


def post_item_to_pinterest(listing, username, title, access_token):
    title = "-".join(title.split())

    item_dictionary = {
        "access_token": access_token,
        "board": username + "/" + title.lower(),
        "note": listing["price"] + " " + listing["title"],
        "link": listing["itemUrl"],
        "image_url": listing["pictureURL"],
    }

    response = requests.post(api_url + "v1/pins/", params=item_dictionary)
    response_data = json.loads(response.text)
    try:
        return response_data["data"]["url"]
    except TypeError:
        return render_template(
            "no_success.html",
            error=(response, response_data),
            no_success_gif=giphy.get_gif("uh oh"),
        )
    except Exception:
        print("Unexpected error:" + response + response_data)
        

def create_pinterest_board(title, access_token):
    item_dictionary = {"access_token": access_token, "name": title}
    response = requests.post(api_url + "v1/boards/", params=item_dictionary)
    response_data = json.loads(response.text)
    if 'url' in response_data:
        return response_data["url"]
    elif 'collaborator_invites_enabled' in response_data:
        return None
    elif 'message' in response_data:
        return response_data['message']
    else:
        return  "Other Error"


if __name__ == "__main__":
    # authenticate_user()
   # get_access_token('229c88a52aeb5f3d')
    print(create_pinterest_board('something', 'AnTY1a6m9QULh1He77v7EU8OjOpRFYsVIss4bARFr4fbGYClgAICADAAABAeRa-KXIcgqaYAAAAA'))
