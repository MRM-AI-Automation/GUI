from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
from flask_cors import CORS 
import socket


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for all origins

# Add the CORS middleware to your Flask app
CORS(app)
ROVER_HOST = "10.0.0.11"
ROVER_PORT = 5005

rover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

@app.route('/')
def index():
    return render_template('controller.html')

@socketio.on('gamepad_event')
def handle_gamepad_event(data):
    rover_socket.sendto(data.encode(), (ROVER_HOST, ROVER_PORT))

    print('Received gamepad event:', data)

if __name__ == '__main__':
    app.run(debug=True)
