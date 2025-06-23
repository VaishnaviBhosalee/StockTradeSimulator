from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/research')
def research():
    return render_template('research.html')