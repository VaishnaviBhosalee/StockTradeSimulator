# from flask import request, jsonify
# import requests, os
# from create_app import app

# FINNHUB_KEY = os.getenv("FINNHUB_KEY")
# BASE_URL = "https://finnhub.io/api/v1"

# @app.route('/api/quote')
# def quote():
#     symbol = request.args.get("symbol", "").strip()
#     if not symbol:
#         return jsonify({"error": "No symbol provided"}), 400

#     try:
#         res = requests.get(f"{BASE_URL}/quote", params={
#             "symbol": symbol,
#             "token": FINNHUB_KEY
#         }, timeout=10)
#         res.raise_for_status()
#         return jsonify(res.json())
#     except requests.RequestException as e:
#         return jsonify({"error": "Request failed", "details": str(e)}), 500
