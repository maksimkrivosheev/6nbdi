import time
from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

instances = []
current_index = 0

def check_health():
    while True:
        global instances
        for instance in instances[:]:  # Создаем копию списка для итерации
            try:
                response = requests.get(f'http://{instance}/health')
                if response.status_code != 200:
                    instances.remove(instance)
            except requests.exceptions.RequestException:
                instances.remove(instance)
        time.sleep(5)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"instances": instances})

@app.route('/process', methods=['GET'])
def process():
    global current_index
    if not instances:
        return jsonify({"error": "No available instances"}), 503
    instance = instances[current_index]
    current_index = (current_index + 1) % len(instances)
    response = requests.get(f'http://{instance}/process')
    return jsonify(response.json())

@app.route('/')
def index():
    return '''
    <form action="/add_instance" method="post">
        IP: <input name="ip"><br>
        Port: <input name="port"><br>
        <input type="submit" value="Add Instance">
    </form>
    <br>
    Current instances: {}
    '''.format(instances)

@app.route('/add_instance', methods=['POST'])
def add_instance():
    ip = request.form['ip']
    port = request.form['port']
    instances.append(f'{ip}:{port}')
    return jsonify({"status": "Instance added"}), 200

@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = int(request.form['index'])
    if 0 <= index < len(instances):
        instances.pop(index)
        return jsonify({"status": "Instance removed"}), 200
    return jsonify({"error": "Invalid index"}), 400

if __name__ == '__main__':
    threading.Thread(target=check_health, daemon=True).start()
    app.run(port=5000)
