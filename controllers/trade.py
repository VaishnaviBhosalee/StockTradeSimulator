from flask import render_template, redirect, url_for, request
from models.user import User
from models.user_finance import UserFinance
from models.user_stocks import UserStocks
from models.portfolio_history import PortfolioHistory
from models.transaction_history import TransactionHistory
from datetime import datetime, timezone
from extensions import db
from create_app import app
import finnhub

f_client = finnhub.Client(api_key=app.config['FINNHUB_API_KEY'])

@app.route('/trade/<user_name>/<login_success>', methods=['GET', 'POST'])
def trade(user_name, login_success):
    user = User.query.filter_by(username=user_name).first_or_404()
    finance = UserFinance.query.filter_by(user_id=user.id).first_or_404()

    message = ''
    current_price = 0
    symbol = ''
    stock_name = ''

    if request.method == 'POST':
        symbol = request.form.get('stock_symbol', '').upper()
        action = request.form.get('action', '').lower()
        stock_name = request.form.get('stock_name', '')

        try:
            qty = int(request.form.get('qty'))
        except (ValueError, TypeError):
            message = 'Invalid quantity.'
            return render_template('trade.html', **locals())

        # Fetch live stock price
        live_quote = f_client.quote(symbol)
        current_price = live_quote.get('c', 0)
        if current_price == 0:
            message = f"Could not fetch price for {symbol}."
            return render_template('trade.html', **locals())

        total = round(qty * current_price, 2)
        stock = UserStocks.query.filter_by(user_id=user.id, stock_symbol=symbol).first()

        profit = 0.0

        if action == 'buy':
            if total > finance.current_balance:
                message = "Not enough balance to buy."
                return render_template('trade.html', **locals())

            finance.current_balance -= total
            finance.todays_change -= total

            if stock:
                old_qty = stock.qty
                stock.qty += qty
                stock.total_value += total
                stock.buy_price_of_user = ((stock.buy_price_of_user * old_qty) + (current_price * qty)) / stock.qty
                stock.status = True
            else:
                stock = UserStocks(
                    user_id=user.id,
                    stock_symbol=symbol,
                    stock_name=stock_name or symbol,
                    qty=qty,
                    buy_price_of_user=current_price,
                    total_value=total,
                    status=True
                )
                db.session.add(stock)

        elif action == 'sell':
            if not stock or qty > stock.qty:
                message = "Not enough stock to sell."
                return render_template('trade.html', **locals())

            # Calculate profit
            profit = round((current_price - stock.buy_price_of_user) * qty, 2)

            stock.qty -= qty
            stock.total_value -= total
            finance.current_balance += total
            finance.todays_change += total

            if stock.qty == 0:
                stock.status = False

        # ✅ Add transaction history
        transaction = TransactionHistory(
            user_id=user.id,
            stock_symbol=symbol,
            stock_name=stock_name or symbol,
            action=action,
            qty=qty,
            price=round(current_price, 2),
            total=total,
            profit=profit if action == "sell" else 0.0
        )
        db.session.add(transaction)

        finance.last_updated = datetime.now()
        db.session.commit()

        # Update portfolio history
        total_port = finance.current_balance + sum(s.total_value for s in user.user_stocks if s.status)
        hist = PortfolioHistory(user_id=user.id, date=datetime.now(), value=total_port)
        db.session.add(hist)
        db.session.commit()
        print(hist.date)

        return redirect(url_for('home', user_name=user_name, login_success=login_success))
    
    return render_template('trade.html',
                           user_name=user_name,
                           login_success=login_success,
                           bank_balance=finance.current_balance,
                           symbol=symbol,
                           stock_name=stock_name,
                           current_price=current_price,
                           message=message)
