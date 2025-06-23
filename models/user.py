from extensions import db


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(20),nullable=False)
    fullname=db.Column(db.String(100),nullable=False)
    joined_data=db.Column(db.Datetime,unique=True)
    display_name = db.Column(db.String(20), unique=True, nullable=False)
    user_finance=db.relationship('Finance',backref='u')
    
    def __repr__(self):
        return f'<User {self.username}>'
