import secrets
import json
import requests
import urllib



api_url = 'https://api.pinterest.com/'

def authenticate_user():
    
    auth_code_dict = {
        'response_type' : 'code',
        'redirect_uri' : 'https://www.hpltopin.com/success/',
        'client_id' : '5021381484636841344',
        'scope' : ['read_public', 'write_public']
    }
    params = urllib.parse.urlencode(auth_code_dict)
    url = api_url + 'oauth/?' + params
    print(url)
    
    
    
def get_access_token(code):
    access_token = {
        'grant_type' : 'authorization_code',
        'client_id' : secrets.pinterest_app_id,
        'client_secret' : secrets.pinterest_token,
        'code' : code

    }
    response = requests.post(api_url + 'v1/oaut/token',params=access_token)
    response_json = response.json()
    return response_json
    
    


def post_item_to_pinterest(listing, title, access_token):
    pinterest_username = 'kevinbigfoot'
    board_name = 'test'
    title = '-'.join(title.split())


    item_dictionary = {
        'access_token' : access_token,
        'board': pinterest_username + '/' + title,
        'note': listing['price'] + ' ' + listing['title'],
        'link': listing['itemUrl'],
        'image_url': listing['pictureURL']
        }


    response = requests.post(api_url + 'v1/pins/',params=item_dictionary)

    response_json = response.json()
    return response_json

def create_pinterest_board(title):

    item_dictionary = {
        'access_token' : secrets.pinterest_token,
        'name' : title
    }
    response = requests.post(api_url + 'v1/boards/',params=item_dictionary)
    response_json = response.json()
    return response_json

if __name__ == '__main__':
    authenticate_user()