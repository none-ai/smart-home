from flask import Flask, render_template, jsonify, request, g
import random
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Request ID middleware
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{g.request_id}] {request.method} {request.path}")

@app.after_request
def after_request(response):
    logger.info(f"[{g.request_id}] Status: {response.status_code}")
    response.headers['X-Request-ID'] = g.request_id
    return response

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'request_id': g.request_id}), 200

# 模拟设备
devices = [
    {"id": 1, "name": "客厅灯", "type": "light", "on": False, "brightness": 80},
    {"id": 2, "name": "空调", "type": "ac", "on": True, "temp": 24},
    {"id": 3, "name": "窗帘", "type": "curtain", "on": False, "open": 0},
    {"id": 4, "name": "摄像头", "type": "camera", "on": True},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/devices')
def get_devices():
    return jsonify(devices)

@app.route('/api/device/<int:device_id>', methods=['POST'])
def control_device(device_id):
    data = request.json
    for d in devices:
        if d['id'] == device_id:
            d.update(data)
            return jsonify({"success": True, "device": d})
    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
