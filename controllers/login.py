from flask import render_template, redirect, request, url_for, session
from create_app import app
from extensions import db
from models.user import User
from datetime import datetime

@app.route('/login', methods=['POST', 'GET'])
def login():
    current_time = datetime.now()

    if request.method == 'POST':
        user_user_name = request.form['user_name']
        user_pass_word = request.form['pass_word']

        user = User.query.filter(
            User.username == user_user_name,
            User.password == user_pass_word
        ).first()

        if user:
            url = url_for('home', user_name=user.username, login_success=True)
            return redirect(url)
        else:
            return render_template('login.html', login_success1=False, current_time=current_time)

    return render_template('login.html', login_success1=True, current_time=current_time)
