import json
from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import os

# Only initialize once
if not firestore._apps:
    cred = credentials.ApplicationDefault()  # gunakan default credentials (lebih aman)
    initialize_app(cred)

db = firestore.client()
survey_bp = Blueprint("survey", __name__)

@survey_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    try:
        db.collection("responses").add({
            **data,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        return jsonify({"status": "success", "redirect": "/terimakasih"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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

