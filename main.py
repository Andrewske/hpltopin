from flask import Flask, render_template, request, jsonify, redirect
import pinterest
import bonanza
import urllib



SECRET_KEY = 'development key'


authentication_url = 'https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https%3A%2F%2Fwww.hpltopin.com%2Fsuccess%2F&client_id=5021381484636841344&scope=%5B%27read_public%27%2C+%27write_public%27%5D'

#Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221

app = Flask(__name__)

app.secret_key = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/authenticate_user', methods=['GET', 'POST'])
def authenticate_user():
    try:
        return redirect(authentication_url)
    except:
        return render_template('index.html')
    #if request.method == 'POST':
        #pinterest.authenticate_user()
        
    #else: return "nope"
    
    

@app.route('/success/', methods=['GET', 'POST'])
def create_and_post():  
    code = request.args.get('code')
    hpl_url = request.form['hpl_url']
    return render_template('index.html', access_code=code)
    #access_token = pinterest.get_access_token(code)
    #return access_token
    data = []
    
    if hpl_url != False:
        return render_template('success.html')
    else: 
        return render_template('success.html')
        #listings, title = bonanza.find_listings(hpl_url)
        #listings_info = bonanza.get_items_information(listings)
        #data.append(pinterest.create_pinterest_board(title))
        #for listing in listings_info:
        #    data.append(pinterest.post_item_to_pinterest(listing, title, access_token)) 
    #return data
            


if __name__ == '__main__':
	app.run(debug=True)


#1. User enters the URL for the HPL
#2. We send them to the Pinterest Authentication
#3. Pinterest returns them to the redirect url with an access token
# Example: https://andrewske.github.io/pinterest-bonanza-api/?state=768uyFys&code=f3bb9c23



