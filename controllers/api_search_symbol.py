from flask import request, jsonify
import requests, os
from create_app import app

FINNHUB_KEY = os.getenv("FINNHUB_KEY")
BASE_URL = "https://finnhub.io/api/v1"

@app.route('/api/search')
def search_symbol():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        res = requests.get(f"{BASE_URL}/search", params={
            "q": query,
            "token": FINNHUB_KEY
        }, timeout=10)
        res.raise_for_status()
        return jsonify(res.json().get("result", []))
    except requests.RequestException as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500
