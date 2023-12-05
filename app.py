from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from os.path import join, dirname, realpath
from database import db
from controller.index import index_app
from controller.login import login_app
from controller.location import location_app

app = Flask(__name__)
app.register_blueprint(index_app)
app.register_blueprint(login_app)
app.register_blueprint(location_app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

UPLOADS_PATH = join(dirname(realpath(__file__)), './static/img/location')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app.run()
