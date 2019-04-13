from .secrets import giphy_api_key
from urllib import request
import json, urllib, requests
import os

api_url = "https://api.giphy.com/v1/gifs/"


def get_gif(keyword):
    if keyword == "ah ah ah":
        return "https://media.giphy.com/media/5ftsmLIqktHQA/giphy.gif"

    item_dictionary = {"api_key": giphy_api_key, "tag": keyword}
    response = requests.get(api_url + "random", params=item_dictionary)
    gif_data = json.loads(response.text)
    # print(json.dumps(gif_data, indent=4, sort_keys=True))
    try:
        return gif_data["data"]["images"]["original"]["url"]
    except:
        if keyword == "success":
            return "https://media.giphy.com/media/dIxkmtCuuBQuM9Ux1E/giphy.gif"
        elif keyword == "uh oh":
            return "https://media.giphy.com/media/w0mylo7p4OXUQ/giphy.gif"
        elif keyword == "welcome":
            return "https://media.giphy.com/media/juBt25nT1KGys/giphy.gif"
        else:
            return "https://media.giphy.com/media/l0IyjeA5mmMZjhyPm/giphy.gif"


if __name__ == "__main__":
    from secrets import giphy_api_key

    get_gif("success")
