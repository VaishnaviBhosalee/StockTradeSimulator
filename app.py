from flask import Flask,render_template,request,redirect,url_for,session
from create_app import app
from extensions import db


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db.init_app(app)

@app.route('/')
def landingPage():
    return "THIS IS Landing Page"


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
