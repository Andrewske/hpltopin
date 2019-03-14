import secrets
import json
import requests


class Pinterest(self):
    def __init__(self):
        self.api_url = 'https://api.pinterest.com/v1/pins/'

    def post_item_to_pinterest(self, listing, pinterest_username, board_name):


        listing = {
            'title': 'MVMT Men\'s Watches | Blacktop Collection | Starlight Black | 47mm | SALE',
            'price': '170.0',
            'itemURL': 'https://www.bonanza.com/listings/MVMT-Men-s-Watches-Blacktop-Collection-Starlight-Black-47mm-SALE/644198149',
            'imageURL': 'https://images.bonanzastatic.com/afu/images/42ea/9902/42cb_6741852984/star1.jpg'
            }

        item_dictionary = {
            'access_token' : secrets.pinterest_token,
            'board': self.pinterest_username + '/' + self.board_name,
            'note': self.listing['price'] + ' ' + self.listing['title'],
            'link': self.listing['itemURL'],
            'image_url': self.listing['imageURL']
            }


        response = requests.post(self.api_url + 'pins/',params=item_dictionary)
        response_json = response.json()
        print(response_json)

    def create_pinterest_board(self, title):

        item_dictionary = {
            'access_token' : secrets.pinterest_token,
            'name' : title
        }
        response = requests.post(self.api_url + 'boards/',params=item_dictionary)
        response_json = response.json()
        print(response_json)
        
p = Pinterest()

p.post_item_to_pinterest()
