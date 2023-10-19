#most comments are tcp/ip shit

from flask import Flask, render_template
from flask_socketio import SocketIO
import rospy
import socket
import threading
from sensor_msgs.msg import NavSatFix

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

latest_imu_data = {}

latest_gps_data = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_imu_data')
def handle_request_imu_data():
    socketio.emit('imu_data', latest_imu_data)

@socketio.on('request_gps_data')
def handle_request_gps_data():
    socketio.emit('gps_data', latest_gps_data)
    
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
    server_socket.bind(('192.168.104.172', 7777))
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