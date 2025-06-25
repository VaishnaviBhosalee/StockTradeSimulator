from extensions import db


class UserStocks(db.Model):
    __tablename__='stocks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    stock_name = db.Column(db.String(50))
    buy_price_of_user = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    stock_symbol = db.Column(db.String(50))
    total_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)
    # Active = True, Inactive = False
    __table_args__ = (
        db.UniqueConstraint('user_id', 'stock_symbol', name='user_stock_unique'),
    )
    def __repr__(self):
        return f'<Stock {self.id}>'