from flask import Flask, request, render_template
from endpoints import *

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/create')
def createIndex():
    return render_template('create.html')

@app.route('/endpoints/lists')
def getList():
    # DUHHH IM SAM AND THINK THAT WE SHOULD USE AUTH HEADERS FOR USER ID
    headers = request.headers
    auth = headers.get("X-Api-Key")
    return lists.getLists(auth)

@app.route('/endpoints/list/<list_id>')
def getListDetails(list_id):
    return list_details.getListDetails(list_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
