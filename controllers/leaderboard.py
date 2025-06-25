from flask import render_template
from datetime import datetime, date
from create_app import app
from extensions import db
from models.user import User, UserFinance, UserStocks
import finnhub

f_client = finnhub.Client(api_key=app.config['FINNHUB_API_KEY'])

@app.route('/leaderboard/<user_name>/<login_success>')
def leaderboard(user_name, login_success):
    users = User.query.all()
    account_balance = []
    today = date.today()
    live_quotes = {}

    for user in users:
        finance = UserFinance.query.filter_by(user_id=user.id).first()
        user_stocks = UserStocks.query.filter_by(user_id=user.id, status=True).all()

        if not finance:
            continue

        total_portfolio_value = finance.current_balance
        todays_stock_change = 0.0

        for stock in user_stocks:
            try:
                if stock.stock_symbol not in live_quotes:
                    live_quotes[stock.stock_symbol] = f_client.quote(stock.stock_symbol)
                quote = live_quotes[stock.stock_symbol]
                current_price = quote.get('c', stock.buy_price_of_user)
                prev_close = quote.get('pc', stock.buy_price_of_user)

                stock.total_value = round(current_price * stock.qty, 2)
                total_portfolio_value += stock.total_value

                if finance.last_updated and finance.last_updated.date() == today:
                    change = (current_price - prev_close) * stock.qty
                    todays_stock_change += change
            except Exception:
                stock.total_value = round(stock.buy_price_of_user * stock.qty, 2)
                total_portfolio_value += stock.total_value

        if finance.last_updated and finance.last_updated.date() == today:
            todays_change = todays_stock_change
        else:
            todays_change = finance.todays_change or 0.0

        change_percent = (todays_change / total_portfolio_value) * 100 if total_portfolio_value != 0 else 0

        account_balance.append({
            'display_name': user.display_name,
            'total_value': round(total_portfolio_value, 2),
            'todays_change': round(todays_change, 2),
            'change_percent': round(change_percent, 2)
        })

    # Sort leaderboard
    account_balance.sort(key=lambda x: x['total_value'], reverse=True)
    
    # Commit once only if needed
    db.session.commit()

    return render_template('leaderboard.html',
                           user_name=user_name,
                           login_success=login_success,
                           current_time=datetime.now(),
                           account_balance=account_balance)
