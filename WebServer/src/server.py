from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("msg", "World")
    return render_template('index.html', msg=name)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)