from flask import Blueprint, request, render_template, session, redirect, url_for
import pymysql
from database import db

index_app = Blueprint('index_app', __name__, template_folder='templates')

@index_app.route('/')
def welcome():
    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    sql = db.sql
    sql_location = db.sql_location
 
    cursor.execute(sql)
    cursor.execute(sql_location)

    cursor.execute('select id, titre, prix, ville, image, created_at from locations limit 2')
    locations = cursor.fetchall()

    return render_template("index.html", locations = locations)

