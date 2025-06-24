from create_app import app
from extensions import db
from flask import render_template,request,jsonify
from dotenv import load_dotenv
import os
from controllers import *
import requests
from datetime import datetime, timedelta
# ---- SET DATABASE BINDS -----------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

load_dotenv()

FINNHUB_KEY = os.getenv("FINNHUB_KEY")




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


import os
import requests
from flask import request, jsonify

@app.route('/api/chart')
def chart():
    symbol = request.args.get("symbol", "").upper()
    api_key = os.getenv("ALPHA_KEY")  # or hardcode for testing

    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key
    }

    res = requests.get(url, params=params)
    data = res.json()

    try:
        ts = data["Time Series (Daily)"]
        dates = list(ts.keys())[::-1][:30]  # last 30 days
        prices = [float(ts[d]["4. close"]) for d in dates]

        return jsonify({
            "t": dates,
            "c": prices
        })
    except:
        return jsonify({"error": "Chart data not available", "api_response": data})



# ---- run the server ----------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
