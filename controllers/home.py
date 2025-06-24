from flask import render_template,redirect
from create_app import app
from extensions import db
from models.user_stocks import UserStocks
from models.user import User

@app.route('/home/<user_name>/<login_success>')
def home(user_name,login_success):
    user = User.query.filter_by(username=user_name).first_or_404()
    stocks = user.user_stocks

    return render_template('home.html',user_name=user_name,login_success=login_success, stocks=stocks)