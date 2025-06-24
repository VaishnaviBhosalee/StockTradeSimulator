from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/learn/<user_name>/<login_success>')
def learn(user_name,login_success):
    return render_template('learn.html', user_name=user_name,login_success=login_success)