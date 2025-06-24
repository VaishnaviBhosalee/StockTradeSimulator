from create_app import app
from extensions import db
from flask import render_template,request,jsonify
from dotenv import load_dotenv
import os
from controllers import *
import requests
# ---- SET DATABASE BINDS -----------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
FINNHUB_KEY = os.getenv("FINNHUB_KEY")

# ---- load secrets -------------------------------------------------
load_dotenv()

# ---- UI ROUTES ----------------------------------------------------
@app.route('/')
def landingPage():
    
    return render_template('landing_page.html')


from flask import request, jsonify
import requests, os
from create_app import app

FINNHUB_KEY = os.getenv("FINNHUB_KEY")
BASE_URL = "https://finnhub.io/api/v1"

@app.route("/api/quote")
def quote():
    symbol = request.args.get("symbol", "").strip().upper()
    
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    try:
        res = requests.get(
            f"{BASE_URL}/quote",
            params={"symbol": symbol, "token": FINNHUB_KEY},
            timeout=10
        )
        res.raise_for_status()
        return jsonify(res.json())
    
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": "HTTP error", "details": str(e)}), 502

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500


@app.route("/api/chart")
def chart():
    symbol = request.args.get("symbol", "").upper()
    res = requests.get("https://finnhub.io/api/v1/stock/candle", params={
        "symbol": symbol,
        "resolution": "D",
        "count": 7,
        "token": FINNHUB_KEY
    })
    return jsonify(res.json())

# ---- run the server ----------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
