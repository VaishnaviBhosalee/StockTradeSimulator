from flask import render_template
from datetime import datetime, timedelta, date
from create_app import app
from extensions import db
from models.user_stocks import UserStocks
from models.user import User
from models.user_finance import UserFinance
from models.portfolio_history import PortfolioHistory
import finnhub

f_client = finnhub.Client(api_key=app.config['FINNHUB_API_KEY'])

@app.route('/home/<user_name>/<login_success>')
def home(user_name, login_success):
    user = User.query.filter_by(username=user_name).first_or_404()
    stocks = user.user_stocks
    finance = UserFinance.query.filter_by(user_id=user.id).first()


    if finance is None:
        finance = UserFinance(user_id=user.id, current_balance=100000, todays_change=0.0)
        db.session.add(finance)
        db.session.commit()

    
    total_portfolio_value = finance.current_balance
    for stock in stocks:
        if stock.status:
            live_quote = f_client.quote(stock.stock_symbol)
            current_price = live_quote.get('c', stock.buy_price_of_user)
            stock.total_value = round(current_price * stock.qty, 2)
            total_portfolio_value += stock.total_value
    db.session.commit()

    
    today = date.today()
    existing_entry = PortfolioHistory.query.filter_by(user_id=user.id, date=today).first()
    if not existing_entry:
        history = PortfolioHistory(user_id=user.id, date=today, value=round(total_portfolio_value, 2))
        db.session.add(history)
        db.session.commit()

   
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    history_data = {h.date: h.value for h in PortfolioHistory.query
                    .filter(PortfolioHistory.user_id == user.id,
                            PortfolioHistory.date.in_(last_7_days))
                    .all()}

    performance_dates = [d.strftime('%a') for d in last_7_days]
    performance_values = [history_data.get(d, total_portfolio_value) for d in last_7_days]

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
