from flask import render_template,redirect
from create_app import app
from extensions import db
from datetime import datetime
@app.route('/trade/<user_name>/<login_success>')
def trade(user_name,login_success):
    current_time = datetime.now()
    return render_template('trade.html', user_name=user_name,login_success=login_success,current_time=current_time)