from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/home')
def home():
    return render_template('home.html')