from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/trade/<user_name>/<login_success>')
def trade(user_name,login_success):
    return render_template('trade.html', user_name=user_name,login_success=login_success)