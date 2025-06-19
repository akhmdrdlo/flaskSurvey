from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import io
import csv
import boto3
import uuid
from datetime import datetime

app = Flask(__name__)

# Koneksi DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('responses')

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
        item = {
            "id": str(uuid.uuid4()),
            **data,
            "timestamp": datetime.utcnow().isoformat()
        }
        table.put_item(Item=item)
        return jsonify({"status": "success", "redirect": "/terimakasih"}), 200
    except Exception as e:
        print(f"DynamoDB error: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 500

@app.route('/admin/export')
def admin_export_page():
    try:
        response = table.scan()
        items = response.get('Items', [])

        data_list = []
        for item in items:
            data_list.append({
                "nama": item.get("nama", ""),
                "role": item.get("role", ""),
                "kelas": item.get("kelas", "-"),
                "provinsi": item.get("provinsi", ""),
                "kabupaten": item.get("kabupaten", "")
            })

        return render_template("export.html", data=data_list)
    except Exception as e:
        print(f"DynamoDB scan error: {e}")
        return "Gagal mengambil data", 500

@app.route('/download_csv')
def download_csv():
    try:
        response = table.scan()
        items = response.get('Items', [])

        # Tentukan urutan kolom
        field_order = [
            "nama", "role", "provinsi", "kabupaten", "kelas"
        ] + [f"q{i}" for i in range(1, 44)] + ["timestamp"]

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=field_order)
        writer.writeheader()

        for item in items:
            row = {key: item.get(key, "") for key in field_order}
            writer.writerow(row)

        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        output.close()

        return send_file(mem, mimetype='text/csv', download_name='hasil_survey.csv', as_attachment=True)
    except Exception as e:
        print(f"DynamoDB CSV export error: {e}")
        return "Gagal menyiapkan file CSV", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
