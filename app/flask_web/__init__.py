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

from app.flask_web import routes_webgui
from app.flask_web import routes_api
