
from flask import Flask, render_template, url_for, request, send_file, session, redirect, flash
from flask_bcrypt import Bcrypt
from app.GraphBuilder import graphBuilder
from app.flask_web.examples import empty, example1, example2
import logging
import json
import os
from app.flask_web.forms import HomeForm, LoadForm, PatchForm, RelateForm, DetachForm
from io import BytesIO
from io import StringIO
from app.flask_web import app


@app.route("/api/v1/drawtree", methods=["GET", "POST"])
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


@app.route("/api/v1/loadcsv", methods=["POST"])
def api_loadcsv():
    try:
        logging.debug('Getting JSON from request object')
        data = request.get_json()

        datastructure = data['datastructure']
        csv = data['csv']

        g = graphBuilder()
        g.loadServiceTreeFromJSON(datastructure)
        g.setServiceArrayFromCSV(csv)

        return app.response_class(response=json.dumps(g.serviceTree.getServiceTreeAsJSON()), status=200, mimetype="application/json")
    except Exception as e:
        return "Something went bad..." + str(e), 500


@app.route("/api/v1/relate", methods=["POST"])
def api_relate():
    try:
        logging.debug('Getting JSON from request object')
        data = request.get_json()

        datastructure = data['datastructure']
        relation = data['relation']

        g = graphBuilder()
        g.loadServiceTreeFromJSON(datastructure)
        g.serviceTree.relations.append(relation)

        return app.response_class(response=json.dumps(g.serviceTree.getServiceTreeAsJSON()), status=200, mimetype="application/json")
    except Exception as e:
        return "Something went bad..." + str(e), 500


@app.route("/api/v1/detach", methods=["POST"])
def api_detach():
    try:
        logging.debug('Getting JSON from request object')
        data = request.get_json()

        datastructure = data['datastructure']
        relation = data['relation']

        g = graphBuilder()
        g.loadServiceTreeFromJSON(datastructure)

        g.serviceTree.deleteRelation(
            relation['provider'], relation['consumer'], relation['type'])

        return app.response_class(response=json.dumps(g.serviceTree.getServiceTreeAsJSON()), status=200, mimetype="application/json")
    except Exception as e:
        return "Something went bad..." + str(e), 500


@app.route("/api/v1/reset/services", methods=["POST"])
def api_reset_services():
    try:
        logging.debug('Getting JSON from request object')
        data = request.get_json()

        datastructure = data['datastructure']

        g = graphBuilder()
        g.loadServiceTreeFromJSON(datastructure)

        g.serviceTree.services = []

        return app.response_class(response=json.dumps(g.serviceTree.getServiceTreeAsJSON()), status=200, mimetype="application/json")
    except Exception as e:
        return "Something went bad..." + str(e), 500


@app.route("/api/v1/reset/relations", methods=["POST"])
def api_reset_relations():
    try:
        logging.debug('Getting JSON from request object')
        data = request.get_json()

        datastructure = data['datastructure']

        g = graphBuilder()
        g.loadServiceTreeFromJSON(datastructure)

        g.serviceTree.relations = []

        return app.response_class(response=json.dumps(g.serviceTree.getServiceTreeAsJSON()), status=200, mimetype="application/json")
    except Exception as e:
        return "Something went bad..." + str(e), 500
