from . import secrets, templates
import requests, json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Pinterest:
    def __init__(self):
        self.api_url = "https://api.pinterest.com/"
        self.access_token = None
        self.username = None
        self.board_name = None

    def get_auth_url(self):
        auth_code_dict = {
            "response_type": "code",
            "redirect_uri": "https://127.0.0.1:5000/authenticate_user",
            "client_id": secrets.bonz_pinterest_app_id,
            "scope": "read_public, write_public, read_relationships, write_relationships",
        }
        params = urlencode(auth_code_dict, True)
        return self.api_url + "oauth/?" + params

    def get_access_token(self, code):
        access_token_dict = {
            "grant_type": "authorization_code",
            "client_id": secrets.bonz_pinterest_app_id,
            "client_secret": secrets.bonz_pinterest_app_secret_key,
            "code": code,
        }
        response = requests.post(
            self.api_url + "v1/oauth/token", data=access_token_dict
        )
        if "access_token" in json.loads(response.text):
            self.access_token = json.loads(response.text)["access_token"]
            return None
        else:
            return json.loads(response.text)

    def set_username(self):
        username_dict = {"access_token": self.access_token, "fields": "username"}
        response = requests.get(self.api_url + "v1/me", params=username_dict)
        user_data = json.loads(response.text)
        try:
            self.username = user_data["data"]["username"]
        except:
            return (response, user_data)

    def post_item_to_pinterest(self, listing):
        item_dictionary = {
            "access_token": self.access_token,
            "board": self.username + "/" + self.board_name,
            "note": listing["price"] + " " + listing["title"],
            "link": listing["itemUrl"],
            "image_url": listing["pictureURL"],
        }
        response = requests.post(self.api_url + "v1/pins/", params=item_dictionary)
        response_data = json.loads(response.text)
        try:
            return response_data["data"]["url"]
        except:
            return response_data

    def create_pinterest_board(self, title):
        item_dictionary = {"access_token": self.access_token, "name": title}
        self.board_name = "-".join(title.split()).lower()
        response = requests.post(self.api_url + "v1/boards/", params=item_dictionary)
        response_data = json.loads(response.text)
        if "data" in response_data:
            if "url" in response_data:
                return response_data["data"]["url"]
        elif "slug" in response_data["message"]:
            return "https://www.pinterest.com/" + self.username + "/" + self.board_name
        else:
            return response_data

    def get_user_info(self):
        username_dict = {
            "access_token": "Ata0gPkksPFjJSLxFBGma0jV5fh2FY9ZD9Sp17ZFr4fbGYClgACaADAAAAA0RbURD3sgt4gAAAAA"
        }
        response = requests.get(self.api_url + "v1/me/", params=username_dict)
        user_data = json.loads(response.text)
        try:
            self.username = user_data["data"]["username"]
        except:
            return (response, user_data)


if __name__ == "__main__":
    p = Pinterest()
    print(p.get_user_info())
