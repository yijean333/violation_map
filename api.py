from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # 允許所有來源跨域請求

VIOLATION_LOG = "violations.json"

# === 路由: 查詢某攝影機違規紀錄 ===
@app.route('/violations/<camera_name>', methods=['GET'])
def get_violations(camera_name):
    try:
        with open(VIOLATION_LOG, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'violations.json not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'JSON decode error'}), 500

    records = data.get(camera_name, [])
    return jsonify(records)

# === 路由: 上傳違規紀錄 ===
@app.route('/upload', methods=['POST'])
def upload_violation():
    try:
        violation = request.get_json()
        if not violation:
            return jsonify({'error': 'Missing JSON payload'}), 400

        camera_name = violation.get("camera_name")
        if not camera_name:
            return jsonify({'error': 'Missing camera_name'}), 400

        if os.path.exists(VIOLATION_LOG):
            with open(VIOLATION_LOG, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        if camera_name not in data:
            data[camera_name] = []

        data[camera_name].append(violation)

        with open(VIOLATION_LOG, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === 主程式啟動 ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
