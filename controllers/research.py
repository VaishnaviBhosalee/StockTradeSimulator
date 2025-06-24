from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/research/<user_name>/<login_success>')
def research(user_name,login_success):
    return render_template('research.html', user_name=user_name,login_success=login_success)