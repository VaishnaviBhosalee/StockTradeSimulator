from flask import request, jsonify, render_template
import requests, os
from create_app import app

@app.route('/')
def landingPage():
    
    return render_template('landing_page.html')

BASE_URL = "https://finnhub.io/api/v1"

@app.route("/api/quote")
def quote():
    symbol = request.args.get("symbol", "").strip().upper()
    
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    try:
        res = requests.get(
            f"{BASE_URL}/quote",
            params={"symbol": symbol, "token": app.config['FINNHUB_API_KEY']},
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