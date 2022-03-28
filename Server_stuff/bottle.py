from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/tuna", methods=["GET"])
def fish_me():
    info = jsonify({'ip': request.remote_addr}), 200
    print(request.remote_addr)
    return info


app.run()
