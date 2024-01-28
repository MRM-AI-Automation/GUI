#most comments are tcp/ip shit
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import time
import cv2
import base64
import json
from threading import Thread
from flask_cors import CORS
from camera import VideoCamera

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=5, ping_interval=2, reconnection=True, reconnection_attempts=3, reconnection_delay=1000, reconnection_timeout=5000)
CORS(app) 

latest_imu_data = {}

latest_gps_data = {}

last_data_time = time.time()

connected_clients = 0  

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    print("sending")
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('save_data')
def handle_save_data(data):
    frame = data.get('frame', '')
    imu_data = data.get('imuData', {})
    gps_data = data.get('gpsData', {})

    save_image(frame, 'saving/captured_image.jpg')

    save_to_file('saving/captured_imu_data.txt', json.dumps(imu_data))
    save_to_file('saving/captured_gps_data.txt', json.dumps(gps_data))

def save_image(data_url, filename):
    # Extract the base64 encoded image data
    _, encoded = data_url.split(',', 1)

    # Decode and save the image
    with open(filename, 'wb') as file:
        file.write(base64.b64decode(encoded))

def save_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(data + '\n')

@socketio.on('connect')
def handle_connect():
    global connected_clients
    connected_clients += 1
    print(f'Client connected. Total connected clients: {connected_clients}')

@socketio.on('disconnect')
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    print(f'Client disconnected. Total connected clients: {connected_clients}')

def check_connection():
    global last_data_time, connected_clients
    RECONNECT_TIMEOUT = 5000
    if time.time() - last_data_time > RECONNECT_TIMEOUT and connected_clients == 0:
        print('No data received and no clients connected. Closing connection.')
        socketio.disconnect()
        
def capture_frames(camera, emit_event):
    while True:
        _, frame = camera.read()
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')
        socketio.emit(emit_event, {'frame': frame_bytes, 'camera': emit_event})


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('update_data')
def handle_update_data(data):
    # print('Received data:', data)
    socketio.emit('sensor_data', data)

if __name__ == '__main__':
    socketio.run(app, debug=False)
        
    #multithreadin
    # rospy.init_node('gps_listener', anonymous=True)
    # socketio.start_background_task(generate_frames)

    # tcp_thread = threading.Thread(target=udp_server)
    # tcp_thread.start()

    # gps_thread = threading.Thread(target=gps_data_listener)
    # gps_thread.start()
    
    #socketio.run(app, host="192.168.51.172", debug=False)
