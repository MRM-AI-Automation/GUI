from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

latest_sensor_data = {}


# Sample data structure, replace this with your actual sensor data
@socketio.on('sensor_data')
def handle_sensor_data(data):
    global latest_sensor_data
    latest_sensor_data = data
    socketio.emit('sensor_data', data)


@app.route('/')
def index():
    return render_template('science.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
