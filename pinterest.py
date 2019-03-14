import secrets
import json
import requests


class Pinterest():
    def __init__(self):
        self.api_url = 'https://api.pinterest.com/v1/pins/'

    def post_item_to_pinterest(self):

        headers = {
            'Content-Type' : 'application/json; charset=utf-8'
        }
        
        username = 'kevinbigfoot'
        boardname = 'test'

        listing = {'title': "MVMT Men's Watches | Blacktop Collection | Starlight Black | 47mm | SALE", 'price': '170.0', 'itemURL': 'https://www.bonanza.com/listings/MVMT-Men-s-Watches-Blacktop-Collection-Starlight-Black-47mm-SALE/644198149', 'imageURL': 'https://images.bonanzastatic.com/afu/images/42ea/9902/42cb_6741852984/star1.jpg'}

        item_dictionary = {'access_token' : secrets.pinterest_token, 'board': username + '/' + boardname, 'note': listing['title'], 'link': listing['itemURL'], 'image_url': listing['imageURL']}

        payload = json.dumps(item_dictionary)

        response = requests.post(self.api_url,params=payload, headers=headers)

        response_json = response.json()

        print(response)

p = Pinterest()

p.post_item_to_pinterest()
