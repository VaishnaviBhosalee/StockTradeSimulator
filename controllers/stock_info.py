from flask import jsonify
from create_app import app
import finnhub

app.config.from_object('config.Config')
f_client = finnhub.Client(api_key=app.config['FINNHUB_API_KEY'])

@app.route('/api/stock-info/<symbol>')
def stock_info(symbol):
    symbol = symbol.upper().strip()
    if not symbol:
        return jsonify({'error': 'Invalid symbol'}), 400

    try:
        profile = f_client.company_profile2(symbol=symbol)
        quote = f_client.quote(symbol)

        if not profile or 'name' not in profile or not quote:
            return jsonify({'error': 'Symbol not found'}), 404

        return jsonify({
            'name': profile.get('name', 'Unknown'),
            'current': quote.get('c', 0.0),
            'prev_close': quote.get('pc', 0.0)  
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
