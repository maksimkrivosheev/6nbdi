from flask import Flask, jsonify
import sys

app = Flask(__name__)

instance_id = None

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "instance_id": instance_id})

@app.route('/process')
def process():
    return jsonify({"instance_id": instance_id})

if __name__ == '__main__':
    instance_id = sys.argv[1]
    port = int(sys.argv[2])
    app.run(port=port)