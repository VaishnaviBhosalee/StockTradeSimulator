# models/portfolio_history.py
from extensions import db
from datetime import datetime, timezone

class PortfolioHistory(db.Model):
    __tablename__ = 'portfolio_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime, default= datetime.now(timezone.utc), nullable=False)
    value = db.Column(db.Float, nullable=False)
