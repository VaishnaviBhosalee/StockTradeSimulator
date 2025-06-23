# controllers/api_search_symbol.py

from flask import request, jsonify
import requests
import os
from create_app import app  # import the central app instance

# Load API key and URL
ALPHA_KEY = os.getenv("ALPHA_KEY")
BASE_URL  = "https://www.alphavantage.co/query"

@app.route('/api/search')
def search_symbol():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": query,
        "apikey": ALPHA_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return jsonify(data.get("bestMatches", []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
