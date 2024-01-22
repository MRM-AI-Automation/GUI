#most comments are tcp/ip shit
import os
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import rospy
import socket
import threading
from sensor_msgs.msg import NavSatFix
import time
import cv2
import base64
import json
from threading import Thread
from flask_cors import CORS
import pickle

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=5, ping_interval=2, reconnection=True, reconnection_attempts=3, reconnection_delay=1000, reconnection_timeout=5000)
CORS(app) 
# app.wsgi_app = socketio.WSGIApp(socketio, app.wsgi_app)

latest_imu_data = {}

latest_gps_data = {}

last_data_time = time.time()

connected_clients = 0  

# cap = cv2.VideoCapture(1)

# def generate():
#     while True:
#         # Read a frame from the webcam
#         ret, frame = cap.read()

#         # Convert the frame to JPEG format
#         _, jpeg = cv2.imencode('.jpg', frame)

#         # Encode the JPEG frame as base64
#         encoded_frame = base64.b64encode(jpeg.tobytes()).decode('utf-8')

#         # Send the frame to the client
#         socketio.emit('video_feed', encoded_frame)

#         # Yield the frame for rendering in the Response
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

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

# @app.route('/video_feed')
# def video_feed():
#     print('doing')
        
# def generate_frames():
#     cap = cv2.VideoCapture(0)  # Use the appropriate camera index
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         # Convert the frame to base64 encoding
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_base64 = base64.b64encode(buffer).decode('utf-8')
#         # print("Sending frame...")
#         socketio.emit('frame', {'data': frame_base64}, namespace='/camera')
#         socketio.sleep(0.03)  # Adjust the delay based on your requirements


# @socketio.on('video_stream')
# def handle_webcam_stream(data):
#     # Broadcast the webcam stream to all connected clients
#     socketio.emit('video_stream', data, broadcast=True)

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

@socketio.on('gps_data')
def handle_gps_data(data):
    global latest_gps_data
    latest_gps_data = {
        'latitude': data.get('latitude', 0),
        'longitude': data.get('longitude', 0),
        'altitude': data.get('altitude', 0),
    }
    socketio.emit('gps_data', latest_gps_data)

@socketio.on('request_imu_data')
def handle_request_imu_data():
    global last_data_time
    last_data_time = time.time()
    socketio.emit('imu_data', latest_imu_data)
    print(connected_clients)

@socketio.on('request_gps_data')
def handle_request_gps_data():
    socketio.emit('gps_data', latest_gps_data)

@socketio.on('save_sensor_data')
def handle_save_sensor_data(sensor_data):
    print("YAYYYYYYYYYYYY")
    try:
        values_line = ','.join(str(value) for sensor in sensor_data.values() for value in sensor.values())

        with open('./saving/sensor_data.txt', 'a') as file:
            file.write(values_line + '\n')

        print('Sensor data saved successfully')
    except Exception as e:
        print(f"Error saving sensor data: {str(e)}")

@socketio.on('save_image')
def save_image(data):
    base64_image = data['base64Image']
    image_data = base64.b64decode(base64_image)

    # Specify the folder and file name to save the image
    folder_path = 'images'
    file_name = 'chart.png'
    file_path = os.path.join(folder_path, file_name)

    # Save the image to the specified folder
    with open(file_path, 'wb') as f:
        f.write(image_data)

    print('Image saved successfully:', file_path)

def check_connection():
    global last_data_time, connected_clients
    RECONNECT_TIMEOUT = 5000
    if time.time() - last_data_time > RECONNECT_TIMEOUT and connected_clients == 0:
        print('No data received and no clients connected. Closing connection.')
        socketio.disconnect()

# webcam = cv2.VideoCapture(0)  # Assuming the webcam is at index 0
# usb_cam = cv2.VideoCapture(2)  # Change the index according to your USB camera

def capture_frames(camera, emit_event):
    while True:
        _, frame = camera.read()
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')
        socketio.emit(emit_event, {'frame': frame_bytes, 'camera': emit_event})

# Start threads to capture frames from both cameras
# webcam_thread = Thread(target=capture_frames, args=(webcam, 'webcam_feed'))
# usb_cam_thread = Thread(target=capture_frames, args=(usb_cam, 'usb_feed'))

# webcam_thread.daemon = True
# usb_cam_thread.daemon = True

# webcam_thread.start()
# usb_cam_thread.start()
    
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/science')
def science():
    return render_template('test_science.html')

@app.route('/react')
def react():
    return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('update_data')
def handle_update_data(data):
    print('Received data:', data)
    socketio.emit('sensor_data', data)


def imu_data_listener(client_socket):
    global latest_imu_data
    
    while True:
        
        try:
            # data = client_socket.recv(1024)
            data, addr = client_socket.recvfrom(1024)
            if not data:
                break
            
            print(data)
            data1 = data.decode("utf-8") 
            data1 = data1.replace("\r", "").replace("\n", "")
            values = data1.split(',')

            # values = data_str.replace("\r", "").replace("\n", "").split(',')

            try:
                values.remove('')
            except ValueError:
                pass

            if len(values) == 9:
                frame_id = 'base_link'

                linear_acceleration_x = float(values[3])
                linear_acceleration_y = float(values[4])
                linear_acceleration_z = float(values[5])

                angular_velocity_x = float(values[0])
                angular_velocity_y = float(values[1])
                angular_velocity_z = float(values[2])

                orientation_x = float(values[6])
                orientation_y = float(values[7])
                orientation_z = float(values[8])

                print(f'Linear Acceleration: x={linear_acceleration_x}, y={linear_acceleration_y}, z={linear_acceleration_z}')
                print(f'Angular Velocity: x={angular_velocity_x}, y={angular_velocity_y}, z={angular_velocity_z}')
                print(f'Orientation: x={orientation_x}, y={orientation_y}, z={orientation_z}')

                latest_imu_data = {
                    'timestamp': time.time(),
                    'linear_acceleration': {
                        'x': linear_acceleration_x,
                        'y': linear_acceleration_y,
                        'z': linear_acceleration_z,
                    },
                    'angular_velocity': {
                        'x': angular_velocity_x,
                        'y': angular_velocity_y,
                        'z': angular_velocity_z,
                    },
                    'orientation':{
                        'x': orientation_x,
                        'y': orientation_y,
                        'z': orientation_z,
                    }
                }

                socketio.emit('imu_data', latest_imu_data)

        except Exception as e:
            print(f"Unexpected error handling IMU data: {e}")
            break


#currently laptop camera, switch around for usb ones
# cap = cv2.VideoCapture(0) 
# def send_camera_frames():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()

#         # Convert the frame to base64 for easy transmission
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_data = base64.b64encode(buffer).decode('utf-8')

#         # Broadcast the frame to all connected clients
#         socketio.emit('camera_frame', frame_data)



# camera_thread = threading.Thread(target=send_camera_frames)
# camera_thread.start()
          
# def gps_data_listener():
#     global latest_gps_data
    
#     def callback(msg):
#         print(msg)
#         global latest_gps_data
#         latest_gps_data = {
#             'latitude': msg.latitude,
#             'longitude': msg.longitude,
#             'altitude': msg.altitude,
#         }
#         socketio.emit('gps_data', latest_gps_data)

#     rospy.Subscriber('/gps/fix', NavSatFix, callback)
#     rospy.spin()

def udp_server():
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('192.168.42.172', 7777))
    # server_socket.bind(('10.57.5.120', 7777))
    # server_socket.listen(1)

    print('TCP server listening on port 7777')

    while True:
        # client_socket, addr = server_socket.accept()
        client_socket, client_address = server_socket.recvfrom(1024)

        imu_thread = threading.Thread(target=imu_data_listener, args=(server_socket,))
        imu_thread.start()

if __name__ == '__main__':
    #multithreadin
    # rospy.init_node('gps_listener', anonymous=True)
    # socketio.start_background_task(generate_frames)

    tcp_thread = threading.Thread(target=udp_server)
    tcp_thread.start()

    # gps_thread = threading.Thread(target=gps_data_listener)
    # gps_thread.start()
    
    socketio.run(app, debug=False)