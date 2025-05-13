from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import io
import csv
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firestore-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terimakasih')
def terimakasih():
    return render_template('terimakasih.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    try:
        db.collection('responses').add({
            **data,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return jsonify({"status": "success", "redirect": "/terimakasih"}), 200
    except Exception as e:
        print(f"Firestore error: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 500

@app.route('/admin/export')
def admin_export_page():
    docs = db.collection("responses").stream()

    data_list = []
    for doc in docs:
        d = doc.to_dict()
        data_list.append({
            "nama": d.get("nama", ""),
            "role": d.get("role", ""),
            "kelas": d.get("kelas", "-"),
            "provinsi": d.get("provinsi", ""),
            "kabupaten": d.get("kabupaten", "")
        })

    return render_template("export.html", data=data_list)


@app.route('/download_csv')
def download_csv():
    # Ambil data dari Firestore
    docs = db.collection("responses").stream()

    # Tentukan urutan kolom
    field_order = [
        "nama", "role", "provinsi", "kabupaten", "kelas"
    ] + [f"q{i}" for i in range(1, 44)] + ["timestamp"]

    # Buat file CSV ke memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=field_order)
    writer.writeheader()

    for doc in docs:
        data = doc.to_dict()
        row = {key: data.get(key, "") for key in field_order}
        writer.writerow(row)

    # Siapkan sebagai file download
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    output.close()

    return send_file(mem, mimetype='text/csv', download_name='hasil_survey.csv', as_attachment=True)
