from flask import render_template,redirect
from create_app import app
from extensions import db
from datetime import datetime
from models.user_stocks import UserStocks


@app.route('/trade/<user_name>/<login_success>', methods=['POST','GET'])
def trade(user_name,login_success):
    current_time = datetime.now()
    # if request.method == 'POST':
    #     new_stock_name = request.form['stock_name']
    #     new_stock_symbol = request.form['stock_symbol']
    #     new_stock_total_price = request.form['total_price']
    #     new_qty = request.form['qty']
    #     new_stock_indi_price = 

    return render_template('trade.html', user_name=user_name,login_success=login_success,current_time=current_time)