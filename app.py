from create_app import app
from extensions import db
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import requests, os

# ---- load secrets -------------------------------------------------
load_dotenv()                           # reads .env
ALPHA_KEY = os.getenv("ALPHA_KEY")
BASE_URL  = "https://www.alphavantage.co/query"


# ---- ROUTES -------------------------------------------------------
@app.route('/')
def landing_page():
    return "THIS IS Landing Page"

# 1. symbol auto-complete
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

# 2. point-in-time quote
@app.route('/api/quote')
def quote():
    symbol = request.args.get("symbol")
    r = requests.get(BASE_URL, params={
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": os.getenv("ALPHA_KEY")
    }, timeout=10)
    return jsonify(r.json().get("Global Quote", {}))

@app.route("/research")
def research_page():
    return render_template("research.html")

# ---- run the server ----------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
