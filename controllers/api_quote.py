from flask import render_template,redirect
from create_app import app
from extensions import db
import requests, os

@app.route('/api/quote')
def quote():
    symbol = request.args.get("symbol")
    r = requests.get(BASE_URL, params={
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": os.getenv("ALPHA_KEY")
    }, timeout=10)
    return jsonify(r.json().get("Global Quote", {}))