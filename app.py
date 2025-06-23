from create_app import app
from extensions import db
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import requests, os
from controllers import *

# ---- SET DATABASE BINDS -----------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


# ---- load secrets -------------------------------------------------
load_dotenv()                           # reads .env
ALPHA_KEY = os.getenv("ALPHA_KEY")
BASE_URL  = "https://www.alphavantage.co/query"


# ---- ROUTES -------------------------------------------------------
@app.route('/')
def landingPage():
    return render_template('landing_page.html')


# ---- run the server ----------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
