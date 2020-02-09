from flask import Flask, request, render_template
from endpoints import *

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("msg", "World")
    return render_template('index.html', msg=name)

@app.route('/endpoints/lists')
def getList():
    # DUHHH IM SAM AND THINK THAT WE SHOULD USE AUTH HEADERS FOR USER ID
    headers = request.headers
    auth = headers.get("X-Api-Key")
    return lists.getLists(auth)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)