# from flask import render_template,redirect
# from create_app import app
# from extensions import db
# from models.user_stocks import UserStocks
# from models.user import User
# from datetime import datetime
# @app.route('/home/<user_name>/<login_success>')
# def home(user_name,login_success):
#     user = User.query.filter_by(username=user_name).first_or_404()
#     stocks = user.user_stocks
#     current_time = datetime.now()
#     return render_template('home.html',user_name=user_name,login_success=login_success, stocks=stocks,current_time=current_time)

from flask import render_template
from datetime import datetime, timedelta
from create_app import app
from extensions import db
from models.user_stocks import UserStocks
from models.user import User
from models.user_finance import UserFinance
from models.portfolio_history import PortfolioHistory  # optional

@app.route('/home/<user_name>/<login_success>')
def home(user_name, login_success):
    user = User.query.filter_by(username=user_name).first_or_404()
    stocks = user.user_stocks
    finance = UserFinance.query.filter_by(user_id=user.id).first()
    if finance is None:
    # Option 1: create one if missing
        finance = UserFinance(user_id=user.id, current_balance=100000, todays_change=0.0)
        db.session.add(finance)
        db.session.commit()


    # Dummy data for chart (until PortfolioHistory is implemented)
    performance_dates = [(datetime.today() - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    performance_values = [finance.current_balance - i * 100 for i in range(7)]

    return render_template(
        'home.html',
        user_name=user_name,
        login_success=login_success,
        stocks=stocks,
        account_value=round(finance.current_balance, 2),
        todays_change=round(finance.todays_change or 0.0, 2),
        performance_dates=performance_dates,
        performance_values=performance_values
    )

