from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory trade history (temporary, will reset when app restarts)
trade_history = []

@app.route('/')
def home():
    return "Crypto Trading Bot is running on Raspberry Pi!"

@app.route('/trade', methods=['POST'])
def trade():
    try:
        data = request.get_json()

        symbol = data.get("symbol")
        side = data.get("side")
        price = float(data.get("price"))
        qty = float(data.get("qty"))
        pnl = float(data.get("profit_loss", 0.0))

        trade_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "side": side,
            "price": price,
            "qty": qty,
            "profit_loss": pnl
        }

        trade_history.append(trade_entry)

        return jsonify({"status": "success", "trade": trade_entry}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/trades', methods=['GET'])
def get_trades():
    return jsonify(trade_history), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
