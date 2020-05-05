
from flask import Flask, render_template, url_for, request, send_file, session, redirect
from flask_bcrypt import Bcrypt
from app.GraphBuilder import graphBuilder
import logging
import json
import os
from app.flask_web.forms import HomeForm, LoadForm, PatchForm, RelateForm
from io import BytesIO
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df61f5fe12eb40792e85b284ead07d51'
bcrypt = Bcrypt(app)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:\t%(message)s')


@app.route("/", methods=["GET"])
def home():
    form = HomeForm()
    if "datastructure" in session.keys():
        form.view.data = session['datastructure']

    return render_template('home.html', form=form, title="Home"), 200


@app.route("/load", methods=["GET", "POST"])
def load():
    form = LoadForm()
    if form.validate_on_submit():
        session['datastructure'] = form.datastructure.data
        return redirect(url_for('home')), 302
    return render_template('load.html', form=form, title='Load'), 200
    # return "Service is running", 200


@app.route("/patch", methods=["GET", "POST"])
def patch():
    form = PatchForm()
    if form.validate_on_submit():
        g = graphBuilder()
        logging.debug(
            f"datastructure to load: {session['datastructure']}")
        g.loadServiceTreeFromJSON(session['datastructure'])
        logging.debug('datastructure loaded')
        logging.debug(f'CSV input is {form.csv.data}')
        serviceList = g.getServiceArrayFromCSV(form.csv.data)
        logging.debug(f'Service list is {serviceList}')
        g.serviceTree.services = serviceList
        logging.debug("ServiceList loaded")
        session['datastructure'] = g.serviceTree.getServiceTreeAsJSON()
        return redirect(url_for('home')), 302
    return render_template('patch.html', form=form, title='Patch'), 200
    # return "Service is running", 200


@app.route("/relate", methods=["GET", "POST"])
def relate():
    form = RelateForm()
    g = graphBuilder()
    g.loadServiceTreeFromJSON(session['datastructure'])

    services = []
    for s in g.serviceTree.services:
        services.append(s['label'])

    form.consumer.choices = services
    form.provider.choices = services

    # logging.debug(f'Errors: {}')
    if form.is_submitted():
        logging.debug('Is validated on submit')
        label_provider = form.provider.data
        label_consumer = form.consumer.data
        # if form.vital.data:
        #     vital = "vital"
        # else:
        #     vital = "important"

        logging.debug(
            f'Trying to add relations between {label_provider} and {label_consumer}')
        g.serviceTree.addRelation(label_provider, label_consumer, "vital")
        logging.debug('Added relation')

        logging.debug(f'Output is {g.serviceTree.getServiceTreeAsJSON()}')
        session['datastructure'] = g.serviceTree.getServiceTreeAsJSON()
        return redirect(url_for('home')), 302

    return render_template('relate.html', form=form, title="Relate"), 200
    # return "Service is running", 200


@app.route("/persist", methods=["GET"])
def persist():
    # proxy = StringIO

    # proxy.write(json.dumps(session['datastructure']))

    # mem = BytesIO
    # mem.write(proxy.getvalue().encode('utf-8'))
    # mem.seek(0)

    b = BytesIO()

    datastructure = json.dumps(session['datastructure'])

    b.write(datastructure.encode('utf-8'))
    b.seek(0)

    return send_file(b, as_attachment=True, attachment_filename='data.json', mimetype='text/json')
    # return "Service is running", 200


@app.route("/view", methods=["GET"])
def view():
    g = graphBuilder()
    g.loadServiceTreeFromJSON(session['datastructure'])

    b = g.drawGraphForWeb()
    b.seek(0)
    return send_file(b, as_attachment=True, attachment_filename='servicetree.gv.pdf', mimetype='application/pdf')
    # return render_template('view.html'), 200
    # return "Service is running", 200


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


# app.run(debug=debug_flag, host="0.0.0.0", port="8000")
