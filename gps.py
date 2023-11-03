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
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = "10.0.0.11"
PORT = 5005
server_address = (HOST, PORT)
print('Listening on', server_address)
try:
    sock.bind(server_address)
    while True:
        received_data, sender = sock.recvfrom(1024)
        received_data = received_data.decode()
        print("Received data from {}: {}".format(sender, received_data))
except OSError as e:
    print(f"Error: {e}")
finally:
    sock.close()