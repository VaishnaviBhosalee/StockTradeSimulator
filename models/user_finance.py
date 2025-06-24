# from extensions import db

# #leaderboard
# class UserFinance(db.Model):
#     __tablename__='finances'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
#     current_balance = db.Column(db.Float,default=100000)
#     todays_change = db.Column(db.Float)
    
#     def __repr__(self):
#         return f'<Finance {self.id}>'

from datetime import datetime
from extensions import db
class UserFinance(db.Model):
    __tablename__ = 'finances'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    current_balance = db.Column(db.Float, default=100000)
    todays_change = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)  # NEW: useful to show update time
    def __repr__(self):
        return f'<Finance {self.id}>'
