# models/portfolio_history.py
from extensions import db
from datetime import date

class PortfolioHistory(db.Model):
    __tablename__ = 'portfolio_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    date = db.Column(db.Date, default=date.today, nullable=False)
    value = db.Column(db.Float, nullable=False)
