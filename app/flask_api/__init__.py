
from flask_web import routes
from flask import Flask, render_template, url_for
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df61f5fe12eb40792e85b284ead07d51'
bcrypt = Bcrypt(app)
