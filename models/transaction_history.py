# models/transaction_history.py
from extensions import db
from datetime import datetime, timezone

class TransactionHistory(db.Model):
    __tablename__ = 'transaction_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    stock_symbol = db.Column(db.String(50))
    stock_name = db.Column(db.String(100))
    action = db.Column(db.String(4))  # 'buy' or 'sell'
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, default=0.0)  # Only for 'sell'
    timestamp = db.Column(db.DateTime, default= datetime.now())

    def __repr__(self):
        return f"<Transaction {self.id} - {self.action.upper()} {self.stock_symbol}>"
