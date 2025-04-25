from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "TIME GPT bot aktif!"

@app.route('/token-info', methods=['POST'])
def token_info():
    data = request.json
    ca = data.get("ca")
    if not ca:
        return jsonify({"error": "CA adresi eksik"}), 400

    # DexScreener verisi
    dex_url = f"https://api.dexscreener.com/latest/dex/tokens/{ca}"
    dex_data = requests.get(dex_url).json()
    if not dex_data["pairs"]:
        return jsonify({"error": "Dex verisi bulunamadı"}), 404
    pair = dex_data["pairs"][0]

    # Solscan holder sayısı
    solscan_url = f"https://public-api.solscan.io/token/holders?tokenAddress={ca}&limit=1"
    solscan_headers = {'accept': 'application/json'}
    holder_data = requests.get(solscan_url, headers=solscan_headers).json()
    holder_count = holder_data.get("total", "Bilinmiyor")

    return jsonify({
        "Token_Adı": pair['baseToken']['name'],
        "Token_Sembol": pair['baseToken']['symbol'],
        "Fiyat_USD": pair['priceUsd'],
        "Degisim_24s_Yuzde": pair['priceChange']['h24'],
        "Hacim_24s_USD": pair['volume']['h24'],
        "Likidite_USD": pair['liquidity']['usd'],
        "FDV": pair.get('fdv', 'Bilinmiyor'),
        "Holder_Sayısı": holder_count,
        "DEX": pair['dexId'],
        "Grafik_URL": pair['url']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
