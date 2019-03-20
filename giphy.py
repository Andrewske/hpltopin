import secrets
from urllib import request
import json, urllib, requests

api_url = 'https://api.giphy.com/v1/gifs/'


def get_gif(keyword):
    
    item_dictionary = {
        'api_key' : secrets.giphy_api_key,
        'tag' : keyword
    }
    response = requests.get(api_url + 'random', params=item_dictionary)
    gif_data = json.loads(response.text)
    try:
        print(gif_data['data']['images']['downsized_medium']['url'])
    except:
        if keyword == 'success': 
            return 'https://media.giphy.com/media/dIxkmtCuuBQuM9Ux1E/giphy.gif'
        elif keyword == "uh oh":   
            return 'https://media.giphy.com/media/w0mylo7p4OXUQ/giphy.gif'
        else:
            return 'https://media.giphy.com/media/l0IyjeA5mmMZjhyPm/giphy.gif'

if __name__ == "__main__":
    get_gif('success')

