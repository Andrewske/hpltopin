import secrets
import json
import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from flask import Flask, redirect



api_url = 'https://api.pinterest.com/'


def authenticate_user():
    auth_code_dict = {
        'response_type' : 'code',
        'redirect_uri' : 'https://www.hpltopin.com/success',
        'client_id' : secrets.pinterest_app_id,
        'scope' : 'read_public, write_public, read_relationships, write_relationships'
    }
    params = urlencode(auth_code_dict, True)
    auth_url = api_url + 'oauth/?' + params
    return auth_url
    
def get_access_token(code):
    access_token_dict = {
        'grant_type' : 'authorization_code',
        'client_id' : secrets.pinterest_app_id,
        'client_secret' : secrets.pinterest_token,
        'code' : code
    }
    response = requests.post(api_url + 'v1/oauth/token', data=access_token_dict)
    response_data = json.loads(response.text)
    print(response, response_data)
    if 'access_token' in response_data:
        return response_data['access_token']
    else: return response_data
    

def get_username(access_token):
    item_dictionary = {
        'access_token' : access_token,
        'fields' : 'username'
    }
    response = requests.get(api_url + 'v1/me', params=item_dictionary)
    user_data = json.loads(response.text)
    if 'username' in user_data:
        return user_data['username']
    else: return user_data
    
    

def post_item_to_pinterest(listing, username, title, access_token): 
    title = '-'.join(title.split())


    item_dictionary = {
        'access_token' : access_token,
        'board': username + '/' + title.lower(),
        'note': listing['price'] + ' ' + listing['title'],
        'link': listing['itemUrl'],
        'image_url': listing['pictureURL']
        }
    #return item_dictionary

    response = requests.post(api_url + 'v1/pins/', params=item_dictionary)
    response_data = json.loads(response.text)
    print(response, response_data)
    if 'data' in response_data:
        return response_data['data']['url']
    else: return response, response_data, item_dictionary

def create_pinterest_board(title, access_token):
    item_dictionary = {
        'access_token' : access_token,
        'name' : title
    }
    response = requests.post(api_url + 'v1/boards/',params=item_dictionary)
    response_data = json.loads(response.text)
    if 'URL' in response_data:
        return response_data['URL']
    else: return response_data

if __name__ == '__main__':
    pass
    #authenticate_user()
    #get_access_token('eb36ad7f6f08086f')
    #post_item_to_pinterest('AnTY1a6m9QULh1He77v7EU8OjOpRFYsVIss4bARFr4fbGYClgAICADAAABAeRa-KXIcgqaYAAAAA')