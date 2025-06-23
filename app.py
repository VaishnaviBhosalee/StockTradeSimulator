from create_app import app
from extensions import db
from flask import render_template
from dotenv import load_dotenv
import os
from controllers import *

# ---- SET DATABASE BINDS -----------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

# ---- load secrets -------------------------------------------------
load_dotenv()

# ---- Import API route (executes @app.route) ----
import controllers.api_search_symbol

# ---- UI ROUTES ----------------------------------------------------
@app.route('/')
def landingPage():
    return render_template('landing_page.html')

# ---- run the server ----------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
