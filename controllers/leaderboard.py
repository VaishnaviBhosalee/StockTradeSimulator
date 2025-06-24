from flask import render_template,redirect
from create_app import app
from extensions import db
from models.user import User
from models.user_finance import UserFinance
from models.user_stocks import UserStock
from sqlalchemy.sql import func
@app.route('/leaderboard/<user_name>/<login_success>')
def leaderboard(user_name,login_success):
    users = (
        db.session.query(User, func.sum(UserStock.total_value).label("total_value"))
        .outerjoin(UserStock)
        .group_by(User.id)
        .order_by(func.sum(UserStock.total_value).desc())
        .all()
    )
    return render_template('leaderboard.html', user_name=user_name,login_success=login_success,users=users)