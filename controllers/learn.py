from flask import render_template,redirect
from create_app import app
from extensions import db

@app.route('/learn/<user_name>/<login_success>')
def learn(user_name,login_success):
    current_time = datetime.now()
    return render_template('learn.html', user_name=user_name,login_success=login_success,current_time=current_time)