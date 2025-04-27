from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terimakasih')
def terimakasih():
    return render_template('terimakasih.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    # Simpan ke file JSON lokal
    responses_file = "responses.json"
    all_data = []

    if os.path.exists(responses_file):
        with open(responses_file, 'r', encoding='utf-8') as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []

    all_data.append(data)

    with open(responses_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    return jsonify({
        "status": "success",
        "redirect": "/terimakasih"
    }), 200
