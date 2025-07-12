from create_app import app
from extensions import db
# from dotenv import load_dotenv
from controllers import *
from datetime import datetime, timedelta


# ---- SET DATABASE BINDS -----------------------------------------
db.init_app(app)

# load_dotenv()

# ---- run the server ----------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
