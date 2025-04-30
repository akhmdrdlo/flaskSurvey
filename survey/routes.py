import json
import os
from flask import Blueprint, request, jsonify, render_template
from google.cloud import firestore
survey_bp = Blueprint(
    'survey',
    __name__,
)

# Initialize Firestore client
db = firestore.Client()

@survey_bp.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        db.collection('responses').add({
            **data,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return jsonify({"status": "success", "redirect": "/terimakasih"}), 200
    except Exception as e:
        print(f"Firestore error: {e}")
        return jsonify({"error": "Gagal menyimpan data"}), 500
# def submit():
#     data = request.get_json(silent=True)

#     if not data:
#         return jsonify({"error": "Invalid or missing JSON data"}), 400

#     # Simpan ke file responses.json (lokal)
#     responses_file = "responses.json"
#     all_data = []

#     if os.path.exists(responses_file):
#         with open(responses_file, 'r', encoding='utf-8') as f:
#             try:
#                 all_data = json.load(f)
#             except json.JSONDecodeError:
#                 all_data = []

#     all_data.append(data)

#     with open(responses_file, 'w', encoding='utf-8') as f:
#         json.dump(all_data, f, indent=2, ensure_ascii=False)

#     return jsonify({
#         "status": "success",
#         "redirect": "/terimakasih"
#     }), 200

