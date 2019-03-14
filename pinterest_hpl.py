from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import secrets
import time
import pinterest_example
import bonanza
import urllib

#Need to have Docker running
#Postman for Pinterest API

#First I need to request the webpage from the user

hpl_url = "https://www.bonanza.com/hpl/Watch-Yourself/163479" #input("What is the HPL URL? ")


pinterest_profile = "https://www.pinterest.com/"+secrets.pinterest_username+"/boards"
pinterest = "https://www.pinterest.com/"
#Then we need to open this page
driver = webdriver.Chrome()
class Pinterest(object):
    def __init__(self):
        self.http_timeout = 15


    def pinterest_log_in():
        driver.get(pinterest)
        log_in_button = driver.find_element_by_link_text("Already a member? Log in")
        log_in_button.click()
        email = driver.find_element_by_id('email')
        password = driver.find_element_by_id('password')
        email.send_keys(secrets.pinterest_email)
        password.send_keys(secrets.pinterest_password)
        redButton = driver.find_element_by_class_name("SignupButton")
        redButton.click()





    #Take the title of the HPL and create a board
    def create_hpl(url):
        driver.get(url)
        title = driver.title.strip("- Hand Picked List")
        log_in()
        driver.get(pinterest_profile)
        create_board_button = driver.find_element_by_class_name("Jea gjz gpV mQ8 mix xuU zI7 iyn Hsu")
        create_board_button.click()
        name = driver.find_element_by_name("boardName")
        name.send_keys(title)


    #create_hpl(hpl_url)
    listing_url = "https://www.bonanza.com/listings/Romain-Jerome-Titanic-DNA-Ultimate-Tourbillon-120-Hour-reserve-Limited-Ed-9/388627036"

    #Function to create Pin
    def create_pin(listing_url):
        log_in()
        create_pin_button = driver.find_element_by_link_text("Create Pin")
        create_pin_button.click()
        save_from_site_button = driver.find_element_by_link_text("Save from site")
        save_from_site_button.click()
        pin_draft_link = driver.find_element_by_id("pin-draft-link")
        pin_draft_link.send_keys(listing_url)
        choose_a_board_button = driver.find_element_by_link_text("Choose a board")
        choose_a_board_button.click()
        choose_current_board = driver.find_element_by_link_text(title)
        choose_a_board_button.click()

    #create_pin(listing_url)


    def find_url():
        driver.get(url)
        listings = driver.find_elements_by_class_name("image_wrap")
        for listing in listings:
            listing_url = listing.get_attribute("href")
            create_pin(listing_url)
        driver.close()
    #For each item, create Pin

    #create_hpl(hpl_url)
    base = "https://api.pinterest.com/v1/"
    note = "Diesel DZ7273 little daddy white gold dial white leather strap unisex watch"
    link = "https://www.bonanza.com/listings/Diesel-DZ7273-little-daddy-white-gold-dial-white-leather-strap-unisex-watch/660154339"
    board_name = "Watch Yourself"


    def post_to_pinterest():
