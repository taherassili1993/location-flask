from flask import Blueprint, request, render_template, session, redirect, url_for
from flask import current_app as app
import pymysql
import os
from database import db

location_app = Blueprint('location_app', __name__, template_folder='templates')

@location_app.route('/ajouter-location')
def ajouter_location():

    return render_template("ajouter_location.html")

@location_app.route('/ajouter-location', methods = ['POST'])
def location_post():
    titre = request.form.get('titre')
    content = request.form.get('content')
    prix = request.form.get('prix')
    ville = request.form.get('ville')
    f = request.files['image']
    image = f.filename
    user_id = session['id']

    f.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('insert into locations(titre, content, prix, ville, image, user_id, created_at) values(%s, %s, %s, %s, %s, %s, NOW())', (titre, content, prix, ville, image, user_id))
    
    # add the article to the database
    db_conn.commit()

    cursor.execute('select id from locations where titre = %s and content = %s and user_id = %s', (titre, content, user_id))
    findLocation = cursor.fetchone()

    return redirect(url_for('location_app.location', id = findLocation[0]))

@location_app.route('/locations/<id>')
def location(id):
    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('select id, titre, content, prix, ville, image, user_id, created_at from locations where id = %s', (id))
    findLocation = cursor.fetchone()
    if not findLocation:
        return redirect(url_for('index_app.welcome'))

    cursor.execute('select id, name, email from users where id = %s', (findLocation[6]))
    findUser = cursor.fetchone()

    return render_template("location.html", location = findLocation, user = findUser)

@location_app.route('/locations')
def locations():
    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('select id, titre, prix, ville, image, created_at from locations')
    locations = cursor.fetchall()
    return render_template("locations.html", locations = locations)

@location_app.route('/recherche')
def recherche_locations():
    q = username = request.args.get('q')

    if not q:
        return redirect(url_for('index_app.welcome'))

    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute("select id, titre, prix, ville, image, created_at from locations where titre like CONCAT('%%', %s, '%%')  or content like CONCAT('%%', %s, '%%')", (q, q))
    locations = cursor.fetchall()
    return render_template("recherche.html", locations = locations)