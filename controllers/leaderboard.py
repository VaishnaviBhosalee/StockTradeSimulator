from flask import render_template,redirect
from create_app import app
from extensions import db
from models.user import User
@app.route('/leaderboard/<user_name>/<login_success>')
def leaderboard(user_name,login_success):
    users=User.query.all()
    
    return render_template('leaderboard.html', user_name=user_name,login_success=login_success,users=users)