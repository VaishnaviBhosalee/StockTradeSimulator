from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/home/<user_name>/<login_success>')
def home(user_name,login_success):
    return render_template('home.html')