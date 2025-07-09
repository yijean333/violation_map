from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # 允許所有來源跨域請求

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

        data.setdefault(camera_name, []).append(violation)

        with open(VIOLATION_LOG, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # 改成讀環境變數 PORT，沒設定就用 5000
    app.run(host='0.0.0.0', port=port, debug=True)
'''
