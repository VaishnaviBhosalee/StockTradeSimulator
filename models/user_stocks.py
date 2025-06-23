from extensions import db


class Stock(db.Model):
    __tablename__='stocks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    stock_name = db.Column(db.String(50), unique=True)
    buy_price_of_user = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    stock_symbol = db.Column(db.String(50), unique=True)
    total_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)

    
    def __repr__(self):
        return f'<Stock {self.id}>'
