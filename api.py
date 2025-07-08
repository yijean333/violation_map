from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# 全域開放跨域，讓前端可以直接 fetch
CORS(app, resources={r"/violations/*": {"origins": "*"}})

VIOLATION_LOG = "violations.json"

# === 根路由: 回傳 map.html ===
@app.route('/')
def index():
    # 使用絕對路徑確保找到 map.html
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return send_file(os.path.join(dir_path, 'map.html'))

# === 路由: 查詢某攝影機違規紀錄 ===
@app.route('/violations/<camera_name>', methods=['GET'])
def get_violations(camera_name):
    print(f"[LOG] GET /violations/{camera_name}")  # 印出接收到的請求以便 debug
    try:
        with open(VIOLATION_LOG, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'violations.json not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'JSON decode error'}), 500

    records = data.get(camera_name, [])
    return jsonify(records), 200

# === 路由: 上傳違規紀錄 ===
@app.route('/upload', methods=['POST'])
def upload_violation():
    print("[LOG] POST /upload")
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

        data.setdefault(camera_name, []).append(violation)

        with open(VIOLATION_LOG, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'error': str(e)}), 500
'''
if __name__ == '__main__':
    # 啟動伺服器
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
'''
