import secrets
import json
import requests


api_url = 'https://api.pinterest.com/v1/'

def authenticate_user():
    pass


def post_item_to_pinterest(listing, title):
    pinterest_username = 'kevinbigfoot'
    board_name = 'test'
    title = '-'.join(title.split())


    item_dictionary = {
        'access_token' : secrets.pinterest_token,
        'board': pinterest_username + '/' + title,
        'note': listing['price'] + ' ' + listing['title'],
        'link': listing['itemUrl'],
        'image_url': listing['pictureURL']
        }


    response = requests.post(api_url + 'pins/',params=item_dictionary)

    response_json = response.json()
    print(response_json)

def create_pinterest_board(title):

    item_dictionary = {
        'access_token' : secrets.pinterest_token,
        'name' : title
    }
    response = requests.post(api_url + 'boards/',params=item_dictionary)
    response_json = response.json()
    print(response_json)
