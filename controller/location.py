from flask import Blueprint, request, render_template, session, redirect, url_for
from flask import current_app as app
import pymysql
import os
from database import db

location_app = Blueprint('location_app', __name__, template_folder='templates')

@location_app.route('/ajouter-location')
def location():

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

    return redirect(url_for('index_app.welcome'))
    #return redirect(url_for('location_app.location', id = findLocation[0]))
