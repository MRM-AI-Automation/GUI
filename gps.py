# import socket
# import serial
# import time

# # Configure the serial port for your GPS device
# ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port and baud rate

# # Configure the server address and port
# server_address = ('192.168.42.172', 7777)  # Replace 'webserver_ip' with the actual IP address of your web server
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     sock.connect(server_address)

#     while True:
#         # Read GPS data from the device
#         gps_data = ser.readline().decode('utf-8').strip()

#         # Send GPS data to the webserver
#         sock.sendall(gps_data.encode('utf-8'))

#         time.sleep(1)  # Adjust the interval as needed

# finally:
#     sock.close()
#     ser.close()

import socket
from flask_socketio import SocketIO
from flask import Flask

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Specify the IP and port for the UDP server
UDP_HOST = "10.0.0.11"
UDP_PORT = 5005

# Specify the IP and port for the Flask app
FLASK_HOST = "192.168.42.172"
FLASK_PORT = 7777

# Bind the UDP server
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((UDP_HOST, UDP_PORT))

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

try:
    while True:
        received_data, sender = udp_sock.recvfrom(1024)
        received_data = received_data.decode()
        print("Received data from {}: {}".format(sender, received_data))

        # Send the received data to the Flask app
        socketio.emit('gps_data', received_data)

except OSError as e:
    print(f"Error: {e}")

finally:
    udp_sock.close()

if __name__ == '__main__':
    socketio.run(app, host=FLASK_HOST, port=FLASK_PORT, debug=False)
