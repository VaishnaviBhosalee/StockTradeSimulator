from flask import request, jsonify
from create_app import app
from models.user import User
from models.user_finance import UserFinance
from models.user_stocks import UserStocks
from models.portfolio_history import PortfolioHistory
from extensions import db
from datetime import datetime, date

@app.route('/api/execute-trade', methods=['POST'])
def execute_trade():
    data = request.json
    username = data.get('user')
    symbol = data.get('symbol', '').upper()
    name = data.get('name', '')
    action = data.get('action')
    qty = int(data.get('qty', 0))
    price = float(data.get('price', 0))

    if not username or not symbol or qty <= 0 or price <= 0:
        return jsonify(error="Invalid input"), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(error="User not found"), 404

    fin = UserFinance.query.filter_by(user_id=user.id).first()
    if not fin:
        return jsonify(error="Finance record not found"), 404

    total = price * qty
    stock = UserStocks.query.filter_by(user_id=user.id, stock_symbol=symbol).first()

    if action == 'buy':
        if total > fin.current_balance:
            return jsonify(error="Insufficient funds"), 400

        fin.current_balance -= total
        fin.todays_change -= total

        if stock:
            old_qty = stock.qty
            stock.qty += qty
            stock.total_value += total
            stock.buy_price_of_user = ((stock.buy_price_of_user * old_qty) + (price * qty)) / stock.qty
        else:
            stock = UserStocks(
                user_id=user.id,
                stock_symbol=symbol,
                stock_name=name,
                qty=qty,
                buy_price_of_user=price,
                total_value=total,
                status=True
            )
            db.session.add(stock)

    elif action == 'sell':
        if not stock or qty > stock.qty:
            return jsonify(error="Not enough shares to sell"), 400

        stock.qty -= qty
        stock.total_value -= total
        fin.current_balance += total
        fin.todays_change += total

        if stock.qty == 0:
            stock.status = False

    else:
        return jsonify(error="Invalid action"), 400

    fin.last_updated = datetime.utcnow()
    db.session.commit()

    # Update portfolio history
    total_port = fin.current_balance + sum(s.total_value for s in user.user_stocks if s.status)
    hist = PortfolioHistory(user_id=user.id, date=date.today(), value=total_port)
    db.session.add(hist)
    db.session.commit()

    return jsonify(success=True, new_balance=round(fin.current_balance, 2))
