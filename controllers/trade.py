from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/trade')
def trade():
    return render_template('trade.html')