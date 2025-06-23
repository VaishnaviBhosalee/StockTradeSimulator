from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/login')
def login():
    return render_template('/login.html')