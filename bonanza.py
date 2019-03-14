import json
import requests

url = 'https://api.bonanza.com/api_requests/secure_request'

headers = {
    'Content-Type' : 'application/json; charset=utf-8',
    'X-BONANZLE-API-DEV-NAME' : 'iElmtQLpdrVHJ7Z',
    'X-BONANZLE-API-CERT-NAME' : 'jSA8b0otHxRcgWe'
}

listings = ['660154339','669928968','644198149','650819038','668243296']

def get_items_information(listings):
    request_name = 'getMultipleItemsRequest'

    #Turn listings array into dictionary
    item_dictionary = {'itemID' : [i for i in listings]}

    # convert dictionary to json
    payload = json.dumps({ request_name : item_dictionary })

    # make the request to Bonanza
    response = requests.post(url, data=payload, headers=headers)

    # the json response as a dictionary
    response_json = response.json()

    # build array of dictionarys
    listings_information = []

    if response_json['ack'] == 'Success' and 'getMultipleItemsResponse' in response_json:
        for item in response_json['getMultipleItemsResponse']['item']:
                listings_information.append({"title":item['title'], "price": item['currentPrice'],"itemUrl": item['viewItemURL']})
    else:
        print(response_json)

    return listings_information
