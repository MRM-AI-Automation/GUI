from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
from threading import Thread
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

latest_sensor_data = {} 

usb_cam = cv2.VideoCapture(0)  # Change the index according to your USB camera
def capture_frames(camera, emit_event):
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to capture frame")
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')
        socketio.emit(emit_event, {'frame': frame_bytes, 'camera': emit_event})

# Start threads to capture frames from both cameras
# webcam_thread = Thread(target=capture_frames, args=(webcam, 'webcam_feed'))
usb_cam_thread = Thread(target=capture_frames, args=(usb_cam, 'usb_feed'))

# webcam_thread.daemon = True
usb_cam_thread.daemon = True

# webcam_thread.start()
usb_cam_thread.start()

# Sample data structure, replace this with your actual sensor data
@socketio.on('sensor_data', namespace='/')
def handle_sensor_data(data):
    global latest_sensor_data
    latest_sensor_data = data
    socketio.emit('sensor_data', data)


@app.route('/')
def index():
    return render_template('science.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
