
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df61f5fe12eb40792e85b284ead07d51'
bcrypt = Bcrypt(app)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:\t%(message)s')


@app.route("/", methods=["GET"])
def home():
    form = HomeForm()
    
    s = ""

    if "datastructure" in session.keys():
        form.view.data = session['datastructure']
        
        if type(session['datastructure']) == str:
            s = json.loads(session['datastructure'])
        else:
            s = session['datastructure']
        s = json.dumps(s, indent=4)
    return render_template('home.html', form=form, title="Home", s=s), 200


@app.route("/load", methods=["GET", "POST"])
def load():
    form = LoadForm()
    if form.validate_on_submit():
        if form.submit.data:
            if form.datastructure.data == "":
                flash('You must add a datastructure', 'danger')
            else:
                session['datastructure'] = form.datastructure.data
                return redirect(url_for('home')), 302
        elif form.empty.data:
            flash('Empty template loaded','info')
            form.datastructure.data = json.dumps(empty, indent=4)
        elif form.example1.data:
            flash('Example 1 loaded','info')
            form.datastructure.data = json.dumps(example1, indent=4)
        elif form.example2.data:
            flash('Example 2 loaded','info')
            form.datastructure.data = json.dumps(example2, indent=4)

    return render_template('load.html', form=form, title='Load'), 200
    # return "Service is running", 200


@app.route("/patch", methods=["GET", "POST"])
def patch():
    if "datastructure" not in session.keys():
        flash('Please load a datastructure before use','info')
        return redirect(url_for('load')), 302

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
    if "datastructure" not in session.keys():
        flash('Please load a datastructure before use','info')
        return redirect(url_for('load')), 302

    form = RelateForm()

    g = graphBuilder()
    g.loadServiceTreeFromJSON(session['datastructure'])

    services = []
    for s in g.serviceTree.services:
        services.append((s['name'], s['label']))

    form.consumer.choices = services

    form.provider.choices = services

    # logging.debug(f'Errors: {}')
    logging.debug(
        f'ready to validate on submit with provider: {form.provider.data} and consumer: {form.consumer.data}')
    if form.validate_on_submit():
        logging.debug('Is validated on submit')
        label_provider = form.provider.data
        label_consumer = form.consumer.data

        if form.vital.data:
            vital = "vital"
        else:
            vital = "important"

        logging.debug(
            f'Trying to add relations between {label_provider} and {label_consumer}')
        g.serviceTree.addRelation(
            form.provider.data, form.consumer.data, vital)
        logging.debug('Added relation')

        logging.debug(f'Output is {g.serviceTree.getServiceTreeAsJSON()}')
        session['datastructure'] = g.serviceTree.getServiceTreeAsJSON()

        flash(
            f"Relation {form.provider.data} --> {form.consumer.data} created!", "success")
        return redirect(url_for('relate')), 302

    #chart_output = g.drawGraphForDynamicWeb()
    # return render_template('relate.html', form=form, title="Relate", chart_output=chart_output), 200
    return render_template('relate.html', form=form, title="Relate"), 200
    # return "Service is running", 200


@app.route("/detach", methods=["GET", "POST"])
def detach():
    if "datastructure" not in session.keys():
        flash('Please load a datastructure before use','info')
        return redirect(url_for('load')), 302

    form = DetachForm()

    g = graphBuilder()
    g.loadServiceTreeFromJSON(session['datastructure'])

    choices = []
    for r in g.serviceTree.relations:
        choices.append((f'{r["supporter"]} --> {r["consumer"]}',
                        f'{g.serviceTree.getServiceLabelFromName(r["supporter"])} --> {g.serviceTree.getServiceLabelFromName(r["consumer"])}'))

    form.relation.choices = choices

    # logging.debug(f'Errors: {}')
    logging.debug(
        f'ready to validate on submit with relation: {form.relation.data} ')
    if form.validate_on_submit():
        logging.debug('Is validated on submit')

        for idx, r in enumerate(g.serviceTree.relations):
            if f'{r["supporter"]} --> {r["consumer"]}' == form.relation.data:
                g.serviceTree.relations.pop(idx)
                break

        logging.debug('Removed relation')

        logging.debug(f'Output is {g.serviceTree.getServiceTreeAsJSON()}')
        session['datastructure'] = g.serviceTree.getServiceTreeAsJSON()

        flash(f"Relation {form.relation.data} deleted!", "success")

        return redirect(url_for('detach')), 302

    return render_template('detach.html', form=form, title="Relate"), 200
    # return "Service is running", 200


@app.route("/persist", methods=["GET"])
def persist():
    if "datastructure" not in session.keys():
        flash('Please load a datastructure before use','info')
        return redirect(url_for('load')), 302

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
    if "datastructure" not in session.keys():
        flash('Please load a datastructure before use','info')
        return redirect(url_for('load')), 302

    g = graphBuilder()
    g.loadServiceTreeFromJSON(session['datastructure'])

    b = g.drawGraphForWeb()
    b.seek(0)
    return send_file(b, as_attachment=True, attachment_filename='servicetree.gv.pdf', mimetype='application/pdf')
    # return render_template('view.html'), 200
    # return "Service is running", 200


@app.route("/viewonly", methods=["GET"])
def viewonly():
    g = graphBuilder()
    g.loadServiceTreeFromJSON(session['datastructure'])

    b = g.drawGraphForWeb()
    b.seek(0)
    # as_attachment=True, attachment_filename='servicetree.gv.pdf',
    return send_file(b,  mimetype='application/pdf')
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
