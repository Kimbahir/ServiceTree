from flask import Flask, render_template, url_for, request
from flask import send_file
from app.GraphBuilder import graphBuilder
import logging
import json
#from flask_bcrypt import Bcrypt
import os

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:\t%(message)s')

app = Flask(__name__)

debug_flag = False
try:
    devserver = os.environ["devserver"]
    debug_flag = True
except KeyError:
    pass


@app.route("/", methods=["GET"])
def home():
    return "Service is running", 200


@app.route("/drawtree", methods=["GET", "POST"])
def drawTree():
    try:
        logging.debug('Getting JSON from request object')
        data = request.get_json()

        logging.debug(f'Building servicetree')
        g = graphBuilder()
        g.loadServiceTreeFromJSON(data)

        logging.debug(f'Writing/showing file')
        g.drawGraph(filename='output/temp.gv', view=False)

        logging.debug(f'Sending file to user')
        return send_file('output/temp.gv.svg', mimetype='image/svg+xml'), 200
    except Exception as e:
        return "Something went bad... " + str(e), 500
    # return "OK", 200


app.run(debug=debug_flag, host="0.0.0.0", port="8000")
