from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import secrets
import time
import bonanza
import pinterest as p
import urllib
import re
import pandas as pd
from bs4 import BeautifulSoup


#Need to have Docker running
#Postman for Pinterest API

#listings = pd.read_csv('listings.csv')

#listings = listings.to_numpy()




hpl_url = "https://www.bonanza.com/hpl/Spring-into-Men-s-Clothes/163722" #input("What is the HPL URL? ")


pinterest_profile = "https://www.pinterest.com/"+secrets.pinterest_username+"/boards"
pinterest = "https://www.pinterest.com/"

def find_listings(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find_all('a', attrs={'class':'image_wrap'})
    listings = []
    for l in elements:
        href = l.get("href")
        listings.append(re.match('.*?([0-9]+)$', href).group(1))
    title = soup.title.string
    title = title.replace(" - Hand Picked List", "")
    return listings[:10], title


def get_listing_information(listings):
    return bonanza.get_items_information(listings)
    #pass


def post_to_pinterest(listings_info, title):
    p.create_pinterest_board(title)
    for listing in listings_info:
        p.post_item_to_pinterest(listing, title)



def main():
    listings, title = find_listings(hpl_url)
    #listings_info = get_listing_information(listings)
    #post_to_pinterest(listings_info, title)


if __name__ == '__main__':
    main()


''' #V1 implementation with Webdriver, switched to BeautifulSoup
def find_listings_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    elements = driver.find_elements_by_class_name("image_wrap")
    listings = []
    for l in elements:
        href = l.get_attribute("href")
        listings.append(re.match('.*?([0-9]+)$', href).group(1))
    title = driver.title
    title = title.replace(" - Hand Picked List", "")
    driver.close()
    print(listings[:10], title)
'''
