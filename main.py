from flask import Flask, render_template, request, jsonify
import pinterest
import bonanza
import urllib




#Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authenticate_user',methods=['GET', 'POST'])
def authenticate_user():
    if request.method == 'POST':
        return urllib.request.urlopen('https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Fsuccess&client_id=5021381484636841344&scope=%5B%27read_public%27%2C+%27write_public%27%5D')
        hpl_url = request.form
        #pinterest.authenticate_user()
        #return render_template('success.html', hpl_url = hpl_url)
    else: return "nope"
    
    

@app.route('/success/<code>', methods=['GET', 'POST'])
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
	app.run(debug=True, ssl_context=('https/server.crt', 'https/server.key'))


#1. User enters the URL for the HPL
#2. We send them to the Pinterest Authentication
#3. Pinterest returns them to the redirect url with an access token
# Example: https://andrewske.github.io/pinterest-bonanza-api/?state=768uyFys&code=f3bb9c23