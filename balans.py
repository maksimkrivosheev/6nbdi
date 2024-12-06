from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

instances = []
lock = threading.Lock()

def check_health():
    while True:
        with lock:
            for instance in instances:
                try:
                    response = requests.get(f'http://{instance}/health')
                    if response.status_code != 200:
                        instances.remove(instance)
                except:
                    instances.remove(instance)
        time.sleep(5)

@app.route('/health')
def health():
    return jsonify({"instances": instances})

@app.route('/process')
def process():
    with lock:
        if len(instances) == 0:
            return jsonify({"error": "No instances available"}), 503
        instance = instances.pop(0)
        instances.append(instance)
        
    response = requests.get(f'http://{instance}/process')
    return jsonify(response.json())

@app.route('/')
def index():
    return '''
    <form action="/add_instance" method="post">
        IP: <input name="ip"><br>
        Порт: <input name="port"><br>
        <input type="submit" value="Добавить инстанс">
    </form>
    <br>
    Текущие инстансы: {}
    '''.format(instances)

@app.route('/add_instance', methods=['POST'])
def add_instance():
    ip = request.form['ip']
    port = request.form['port']
    with lock:
        instances.append(f'{ip}:{port}')
    return jsonify({"status": "instance added"})

@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = int(request.form.get('index'))
    with lock:
        if 0 <= index < len(instances):
            instances.pop(index)
    return jsonify({"status": "instance removed"})

if __name__ == '__main__':
    threading.Thread(target=check_health).start()
    app.run(port=5000)
