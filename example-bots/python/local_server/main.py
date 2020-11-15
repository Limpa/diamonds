import flask
import time
import requests 
import threading
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
global last_req_data

def update_data():
    global last_req_data
    r = requests.get("http://diamonds.etimo.se/api/boards/2") 
    last_req_data = r.json()
    myThread.run()

@app.route('/', methods=['GET'])
def home():
    global last_req_data
    return jsonify(last_req_data)

if __name__ == '__main__':
    last_req_data = None
    myThread = threading.Timer(0.2, update_data)
    myThread.start()
    app.run()
