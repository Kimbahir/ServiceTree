
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


# @app.route("/showpicture", methods=['GET'])
# def showpicture():

#     b = BytesIO()

#     logging.debug('do we get here?')

#     g = graphBuilder()

#     logging.debug('Trying to get session')

#     g.loadServiceTreeFromJSON(session['datastructure'])

#     logging.debug('Creating output')

#     chart_output = g.drawGraphForDynamicWeb()

#     logging.debug('Ready to return')

#     return render_template('svg.html', chart_output=chart_output)


# app.run(debug=debug_flag, host="0.0.0.0", port="8000")
