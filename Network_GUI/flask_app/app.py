from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

devices = [
    {'name': 'Base Transceiver', 'ip': '10.0.0.8', 'connected': 0},
    {'name': 'NVR', 'ip': '10.0.0.22', 'connected': 0},
    {'name': 'Rover Transceiver', 'ip': '10.0.0.2', 'connected': 0},
    {'name': 'Lan to UART', 'ip': '10.0.0.7', 'connected': 0},
    {'name': 'RPi-1', 'ip': '10.0.0.3', 'connected': 0},
    {'name': 'RPi-2', 'ip': '10.0.0.9', 'connected': 0},
    {'name': 'Jetson', 'ip': '10.0.0.6', 'connected': 0},
]

def ping_devices():
    while True:
        for device in devices:
            device['connected'] = 1 if os.system(f"ping -c 1 -s 1 -q -w 1 {device['ip']} > /dev/null 2> /dev/null") == 0 else 0
        print(devices)
        socketio.emit('update_devices', devices)
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    socketio.emit('update_devices', devices)

if __name__ == '__main__':
    Thread(target=ping_devices).start()
    socketio.run(app)
