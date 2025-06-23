from flask import render_template,redirect
from create_app import app
from extensions import db
import requests, os

@app.route('/api/search')
def search_symbol():
    q = request.args.get("q", "")
    r = requests.get(BASE_URL, params={
        "function": "SYMBOL_SEARCH",
        "keywords": q,
        "apikey": os.getenv("ALPHA_KEY")
    }, timeout=10)
    matches = r.json().get("bestMatches", [])[:10]
    return jsonify([
        {"symbol": m["1. symbol"], "name": m["2. name"], "region": m["4. region"]}
        for m in matches
    ])