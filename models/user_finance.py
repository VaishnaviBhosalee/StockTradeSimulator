from extensions import db

#leaderboard
class UserFinance(db.Model):
    __tablename__='finances'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    current_balance = db.Column(db.Float,default=100000)
    todays_change = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Finance {self.id}>'
