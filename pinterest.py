from flask import Flask, render_template, redirect
from . import secrets, giphy, templates
import json
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


api_url = "https://api.pinterest.com/"
access_token = None
username = None


def authenticate_user():
    auth_code_dict = {
        "response_type": "code",
        "redirect_uri": "https://127.0.0.1:5000/authenticated",
        "client_id": secrets.bonz_pinterest_app_id,
        "scope": "read_public, write_public, read_relationships, write_relationships",
    }
    params = urlencode(auth_code_dict, True)
    auth_url = api_url + "oauth/?" + params
    return auth_url


def get_access_token(code):
    access_token_dict = {
        "grant_type": "authorization_code",
        "client_id": secrets.bonz_pinterest_app_id,
        "client_secret": secrets.bonz_pinterest_app_secret_key,
        "code": code,
    }
    response = requests.post(api_url + "v1/oauth/token", data=access_token_dict)
    response_data = json.loads(response.text)
    if "access_token" in response_data:
        global access_token
        access_token = response_data["access_token"]
        return access_token
    else:
        return response_data


def set_username():
    item_dictionary = {"access_token": access_token, "fields": "username"}
    response = requests.get(api_url + "v1/me/", params=item_dictionary)
    user_data = json.loads(response.text)
    try:
        global username
        username = user_data["data"]["username"]
        return username
    except:
        return response


def post_item_to_pinterest(listing, title):
    if not isinstance(title, str) or not isinstance(username, str):
        return [title, username]
    else:
        title = "-".join(title.split()).lower()
        item_dictionary = {
            "access_token": access_token,
            "board": username + "/" + title,
            "note": listing["price"] + " " + listing["title"],
            "link": listing["itemUrl"],
            "image_url": listing["pictureURL"],
        }
        response = requests.post(api_url + "v1/pins/", params=item_dictionary)
        response_data = json.loads(response.text)
        try:
            return response_data["data"]["url"]
        except:
            return response_data


def create_pinterest_board(title):
    item_dictionary = {"access_token": secrets.pinterest_test_key, "name": title}
    response = requests.post(api_url + "v1/boards/", params=item_dictionary)
    response_data = json.loads(response.text)
    if "data" in response_data:
        if "url" in response_data:
            return response_data["data"]["url"]
    elif "slug" in response_data["message"]:
        title = "-".join(title.split()).lower()
        return "https://www.pinterest.com/" + username + "/" + title
    else:
        return response_data


if __name__ == "__main__":
    # print(authenticate_user())
    set_username()
    print(username)
    # get_access_token('229c88a52aeb5f3d')
    # listing = {'title': 'Hand Made Luxury Cat Eye Sun glasses Women Polarized Sunglasses Goggles UV400 ', 'price': '28.71', 'itemUrl': 'https://www.bonanza.com/listings/Hand-Made-Luxury-Cat-Eye-Sun-glasses-Women-Polarized-Sunglasses-Goggles-UV400/671856167', 'pictureURL': 'https://images.bonanzastatic.com/afu/images/fd49/ac61/6b11_7211986758/__57.jpg'}
    # post_item_to_pinterest(listing,'Shades and Sunnies', 'kevinbigfoot', '648542818')
    # print(
    #     create_pinterest_board(
    #         "test",
    #         "kevinbigfoot",
    #         "AnTY1a6m9QULh1He77v7EU8OjOpRFYsVIss4bARFr4fbGYClgAICADAAABAeRa-KXIcgqaYAAAAA",
    #     )
    # )
