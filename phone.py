from flask import Flask, render_template
from flask_socketio import SocketIO
import socket
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Set CORS origins as needed

# Store the latest IMU data
latest_imu_data = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_imu_data')
def handle_request_imu_data():
    socketio.emit('imu_data', latest_imu_data)
    
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
            
            # print("hi")
            # Decode the received data as UTF-8
            data1 = data.decode("utf-8")  # BYTE TO STRING DECODING USING UTF-8
            data1 = data1.replace("\r", "").replace("\n", "")
            values = data1.split(',')

            # Remove newline characters and split the values
            # values = data_str.replace("\r", "").replace("\n", "").split(',')

            try:
                values.remove('')
            except ValueError:
                pass

            if len(values) == 9:
                # Convert values to IMU message
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

                # Store the latest IMU data
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

                # Emit data to connected clients
                socketio.emit('imu_data', latest_imu_data)

        except Exception as e:
            print(f"Unexpected error handling IMU data: {e}")
            break

def tcp_server():
    #10.90.2.136
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('192.168.64.172', 8910))  # Change the port as needed
    # server_socket.listen(1)

    print('TCP server listening on port 8910')

    while True:
        # client_socket, addr = server_socket.accept()
        client_socket, client_address = server_socket.recvfrom(1024)
        print('Accepted connection from', client_address)

        # Start a new thread to handle IMU data from this client
        # imu_thread = threading.Thread(target=imu_data_listener, args=(client_socket,))
        # imu_thread.start()

        imu_thread = threading.Thread(target=imu_data_listener, args=(server_socket,))
        imu_thread.start()

if __name__ == '__main__':
    # Start the TCP server in a separate thread
    tcp_thread = threading.Thread(target=tcp_server)
    tcp_thread.start()

    # Run the Flask SocketIO app
    socketio.run(app, debug=False)




# from flask import Flask, render_template
# from flask_socketio import SocketIO
# from socket import socket, AF_INET, SOCK_DGRAM
# import threading

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")  # Set CORS origins as needed

# # Store the latest IMU data
# latest_imu_data = {}

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# # @socketio.on('request_imu_data')
# # def handle_request_imu_data():
# #     socketio.emit('imu_data', latest_imu_data)
    
# @app.route('/')
# def index():
#     return render_template('imu.html')

# def imu_data_listener():
#     sock = socket(AF_INET, SOCK_DGRAM)
#     sock.bind(('192.168.227.172', 8916))
#     while True:
#         try:
#             data,addr = sock.recvfrom(8196)
#             socketio.emit('imu_data', data.decode())
#             print(data)
#         except Exception as e:
#             print(f"Unexpected error handling IMU data: {e}")
#             break



# if __name__ == '__main__':

#     # Start the TCP server in a separate thread
#     tcp_thread = threading.Thread(target=imu_data_listener)
#     tcp_thread.start()

#     # Run the Flask SocketIO app
#     socketio.run(app, debug=False)
