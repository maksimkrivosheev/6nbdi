from flask import Flask, jsonify

app = Flask(__name__)

instance_id = None

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "id": instance_id})

@app.route('/process')
def process():
    return jsonify({"instance_id": instance_id})

if __name__ == '__main__':
    import sys
    instance_id = sys.argv[1]
    app.run(port=int(sys.argv[2]))
