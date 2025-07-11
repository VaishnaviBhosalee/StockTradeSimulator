from extensions import db
from datetime import datetime, timezone
from models.user_finance import UserFinance
from models.user_stocks import UserStocks
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    joined_data = db.Column(db.DateTime, default=datetime.now())
    display_name = db.Column(db.String(20), unique=True, nullable=False)
    first_login = db.Column(db.Boolean, default=True, nullable=False)
    user_finance = db.relationship('UserFinance',backref='uf')
    user_stocks = db.relationship('UserStocks',backref='us')
    
    def __repr__(self):
        return f'<User {self.username}>'
