from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/build/char", methods=['POST'])
def hello():
    return request.json

@app.route("/build/mod", methods=['POST'])
def hello2():
    return "Hello Universe!"
