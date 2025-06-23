from flask import render_template,redirect
from create_app import app
from extensions import db
from models.user import User
@app.route('/register')
def register():
    
    return render_template('register.html')