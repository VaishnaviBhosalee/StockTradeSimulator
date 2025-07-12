from flask import request, jsonify
import requests, os
from create_app import app

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