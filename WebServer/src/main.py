import json
import os

from flask import Flask, request, render_template, redirect, url_for
from endpoints import *

from oauthlib.oauth2 import WebApplicationClient
import requests 

import random

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response.json()["sub"])
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create')
def createIndex():
    return render_template('create.html')

@app.route('/lists')
def list_view():
    ret_payload, ret_code = lists.getLists(str(1))
    todo_lists = json.loads(ret_payload)
    print(todo_lists)
    return render_template('lists.html', lists=todo_lists)

@app.route('/endpoints/lists')
def getList():
    # DUHHH IM SAM AND THINK THAT WE SHOULD USE AUTH HEADERS FOR USER ID
    headers = request.headers
    auth = headers.get("X-Api-Key")
    return lists.getLists(auth)

@app.route('/endpoints/lists/<list_id>')
def getListDetails(list_id):
    return list_details.getListDetails(list_id)

@app.route('/endpoints/search')
def makeSearch():
    string = request.args.get('query')
    return search_produce.search_produce(string)

@app.route('/endpoints/add-product')
def add_product():
    skus = request.form.get('skus')
    names = request.form.get('names')
    list_id = random.randint(10, 100)
    return add_product.add_product(list_id, skus, names)


@app.route('/endpoints/products/<entry_id>', methods = ['PUT'])
def updateProduct(entry_id):
    checked = request.args.get('checked')
    checked = checked == 'true'
    auth = request.headers.get("X-Api-Key")
    update_product.put_checked(entry_id, checked)
    return "GOOD"
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
