from flask import Flask, render_template, request, jsonify
import pinterest
import bonanza

#Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def authenticate_user():
    print("auth page")
    pinterest.authenticate_user()
    

@app.route('/sucess/<code>', methods=['GET', 'POST'])
def create_and_post(code):
    access_token = pinterest.get_access_token(code.remove('?code='))
    data = []
    try:
        hpl_url = request.form['hpl_url']
    except:
        hpl_url = False
        print("No hpl_url found")
    if hpl_url != False:
        listings, title = bonanza.find_listings(hpl_url)
        listings_info = bonanza.get_items_information(listings)
        data.append(pinterest.create_pinterest_board(title))
        for listing in listings_info:
            data.append(pinterest.post_item_to_pinterest(listing, title, access_token)) 
    return data
            


if __name__ == '__main__':
	app.run(debug=True)


#1. User enters the URL for the HPL
#2. We send them to the Pinterest Authentication
#3. Pinterest returns them to the redirect url with an access token
# Example: https://andrewske.github.io/pinterest-bonanza-api/?state=768uyFys&code=f3bb9c23