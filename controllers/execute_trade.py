from flask import request, jsonify
from create_app import app
from models.user import User
from models.user_finance import UserFinance
from models.user_stocks import UserStocks
from models.portfolio_history import PortfolioHistory
from extensions import db
from datetime import datetime, date
import finnhub

f_client = finnhub.Client(api_key=app.config['FINNHUB_API_KEY'])

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

        # Update cash balance
        fin.current_balance -= total
        
        # DON'T change todays_change for purchases - it should reflect P&L only
        # todays_change will be calculated based on current stock prices vs purchase prices

        if stock:
            # Update existing stock position
            old_qty = stock.qty
            old_total = stock.total_value
            
            stock.qty += qty
            # Calculate weighted average price
            stock.buy_price_of_user = ((stock.buy_price_of_user * old_qty) + (price * qty)) / stock.qty
            stock.total_value = stock.qty * stock.buy_price_of_user  # Use average price for total value
        else:
            # Create new stock position
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

        # Calculate profit/loss from this sale
        cost_basis = stock.buy_price_of_user * qty
        profit_loss = (price * qty) - cost_basis
        
        # Update stock position
        stock.qty -= qty
        stock.total_value = stock.qty * stock.buy_price_of_user if stock.qty > 0 else 0
        
        # Update cash balance
        fin.current_balance += total
        
        # Update today's change with the realized profit/loss
        fin.todays_change = (fin.todays_change or 0) + profit_loss

        if stock.qty == 0:
            stock.status = False

    else:
        return jsonify(error="Invalid action"), 400

    fin.last_updated = datetime.utcnow()
    
    # Calculate total portfolio value for history
    total_stock_value = 0
    for user_stock in UserStocks.query.filter_by(user_id=user.id, status=True).all():
        try:
            # Get current market price for accurate portfolio value
            live_quote = f_client.quote(user_stock.stock_symbol)
            current_price = live_quote.get('c', user_stock.buy_price_of_user)
            user_stock.total_value = current_price * user_stock.qty
            total_stock_value += user_stock.total_value
        except:
            # Fallback to purchase price if API fails
            user_stock.total_value = user_stock.buy_price_of_user * user_stock.qty
            total_stock_value += user_stock.total_value
    
    db.session.commit()

    # Update portfolio history with current market values
    total_portfolio_value = fin.current_balance + total_stock_value
    
    # Check if there's already a history entry for today
    today_history = PortfolioHistory.query.filter_by(user_id=user.id, date=date.today()).first()
    if today_history:
        today_history.value = total_portfolio_value
    else:
        hist = PortfolioHistory(user_id=user.id, date=date.today(), value=total_portfolio_value)
        db.session.add(hist)
    
    db.session.commit()

    return jsonify(success=True, new_balance=round(fin.current_balance, 2))