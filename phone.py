#most comments are tcp/ip shit

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import rospy
import socket
import threading
from sensor_msgs.msg import NavSatFix
import time
import cv2
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=5, ping_interval=2, reconnection=True, reconnection_attempts=3, reconnection_delay=1000, reconnection_timeout=5000)

latest_imu_data = {}

latest_gps_data = {}

last_data_time = time.time()

connected_clients = 0  

cap = cv2.VideoCapture(0)

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

@socketio.on('webcam_stream')
def handle_webcam_stream(data):
    # Broadcast the webcam stream to all connected clients
    socketio.emit('webcam_stream', data, broadcast=True)

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

def check_connection():
    global last_data_time, connected_clients
    RECONNECT_TIMEOUT = 5000
    if time.time() - last_data_time > RECONNECT_TIMEOUT and connected_clients == 0:
        print('No data received and no clients connected. Closing connection.')
        socketio.disconnect()

    
@app.route('/')
def index():
    return render_template('index.html')

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


def gps_data_listener():
    global latest_gps_data
    
    def callback(msg):
        print(msg)
        global latest_gps_data
        latest_gps_data = {
            'latitude': msg.latitude,
            'longitude': msg.longitude,
            'altitude': msg.altitude,
        }
        socketio.emit('gps_data', latest_gps_data)

    rospy.Subscriber('/gps/fix', NavSatFix, callback)
    rospy.spin()

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
    rospy.init_node('gps_listener', anonymous=True)
    
    tcp_thread = threading.Thread(target=udp_server)
    tcp_thread.start()

    gps_thread = threading.Thread(target=gps_data_listener)
    gps_thread.start()

    socketio.run(app, debug=False)
