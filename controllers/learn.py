from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/learn')
def learn():
    return render_template('learn.html')