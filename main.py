from flask import Flask, render_template, request, jsonify, redirect
import pinterest, bonanza, giphy
import urllib



SECRET_KEY = 'development key'

gifs = ['https://media.giphy.com/media/nXxOjZrbnbRxS/giphy.gif', ]

authentication_url = 'https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https%3A%2F%2Fwww.hpltopin.com%2Fsuccess&client_id=5021381484636841344&scope=%5B%27read_public%27%2C+%27write_public%27%5D'

#Deploying App on Google App Engine - https://medium.freecodecamp.org/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/authenticate_user', methods=['GET', 'POST'])
def authenticate_user(): 
    if request.method == 'POST':
        bonanza.set_hpl(request.form['hpl_url'])
        auth_url = pinterest.authenticate_user()
        return redirect(auth_url)
    else: return render_template('index.html')
    
    

@app.route('/success', methods=['GET', 'POST'])
def create_and_post():
    error = None
    data = []
    access_token = pinterest.get_access_token(request.args.get('code'))
    if "Try Again" in access_token:
        error = access_token
    else:
        username = 'kevinbigfoot' #pinterest.get_username(access_token)
        hpl_url = bonanza.hpl_url
        listings, title = bonanza.find_listings(hpl_url)
        listings_info = bonanza.get_items_information(listings)
        board_url = pinterest.create_pinterest_board(title, access_token)
        for listing in listings_info:
           data.append(pinterest.post_item_to_pinterest(listing,username, title, access_token)) 
    if error == None:
        success_gif = giphy.get_gif('success')
        return render_template('success.html', data=data, username=username, title=title, board_url=board_url, success_gif=success_gif)
    else: return render_template('no_success.html', error=error, no_success_gif=giphy.get_gif('uh oh'))


@app.route('/test', methods=['GET', 'POST'])
def test():
    data = ['https://www.pinterest.com/pin/144678206765760738/',
'https://www.pinterest.com/pin/144678206765760739/']
    username = 'kevinbigfoot'
    title = 'watch-yourself'
    board_url = "https://www.bonanza.com/hpl/Watch-Yourself/163479"
    success_gif = giphy.get_gif('success')
    return render_template(
        'success.html', 
        data=data, 
        username=username, 
        title=title, 
        board_url=board_url, 
        success_gif=success_gif)
            


if __name__ == '__main__':
	app.run(debug=True)


#1. User enters the URL for the HPL
#2. We send them to the Pinterest Authentication
#3. Pinterest returns them to the redirect url with an access token
# Example: https://andrewske.github.io/pinterest-bonanza-api/?state=768uyFys&code=f3bb9c23



