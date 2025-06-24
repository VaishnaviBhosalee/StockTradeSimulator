from flask import render_template, redirect, request, url_for, session
from create_app import app
from extensions import db
from datetime import datetime
from models.user_stocks import UserStocks


@app.route('/trade/<user_name>/<login_success>')
def trade(user_name, login_success):
    current_time = datetime.now()
    return render_template('trade.html', user_name=user_name, login_success=login_success, current_time=current_time)


# Show preview of trade
@app.route('/trade/preview', methods=['POST'])
def trade_preview():
    trade_data = request.form.to_dict()

    # Debug: print keys for confirmation
    print("Received trade data:", trade_data)

    try:
        total = round(float(trade_data.get('total_price', 0)), 2)
    except:
        total = 0

    return render_template('preview.html', trade=trade_data, total=total)


# Final confirmation and saving to DB
@app.route('/trade/confirm', methods=['POST'])
def confirm_trade():
    trade = request.form
    print("Confirming trade data:", dict(trade))  # Debug

    user_id = session.get('user_id')  # ensure set during login

    user_stock = UserStocks(
        user_id=user_id,
        stock_name=trade.get('description'),
        stock_symbol=trade.get('stock_symbol', '').upper(),
        buy_price_of_user=float(trade.get('total_price', 0)) / int(trade.get('qty', 1)),
        qty=int(trade.get('qty', 0)),
        total_value=float(trade.get('total_price', 0)),
        status=True
    )

    db.session.add(user_stock)
    db.session.commit()

    return redirect(url_for('home', user_name=session['username'], login_success='true'))
