from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import secrets
import time
import bonanza
#import pinterest
import urllib
import re

#Need to have Docker running
#Postman for Pinterest API

#First I need to request the webpage from the user

hpl_url = "https://www.bonanza.com/hpl/Watch-Yourself/163479" #input("What is the HPL URL? ")


pinterest_profile = "https://www.pinterest.com/"+secrets.pinterest_username+"/boards"
pinterest = "https://www.pinterest.com/"
#Then we need to open this page
driver = webdriver.Chrome()

class hpl_to_pinterest_board(self, hpl_url):
    def __init__(self):
        self.url = help_url

    def find_listings(self):
        driver.get(self.url)
        listings = driver.find_elements_by_class_name("image_wrap")
        new_list = []
        for l in listings:
            new_list.append(re.match('.*?([0-9]+)$', l))

        driver.close()
        print(new_list)


hpl = hpl_to_pinterest_board()
hpl.find_listings(hpl_url)
