# dummy_data_generator.py
from flask import Flask, render_template, Response
import socketio
import random
import time
from flask_socketio import SocketIO
from sensor_msgs.msg import Image   
from cv_bridge import CvBridge
import rospy
import threading
import socket
import cv2
import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal


# app = Flask(_name_)
sio = socketio.Client()
bridge = CvBridge()


# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


receiver_ip1 = ''
receiver_port1 = 12345

receiver_ip2 = ''
receiver_port2 = 8080

server_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock1.bind((receiver_ip1, receiver_port1))
server_sock1.listen(1)

print(f"Waiting for a connection on {receiver_ip1}:{receiver_port1}")

connection1, sender_address1 = server_sock1.accept()
print(f"Connection established with {sender_address1}")

server_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock2.bind((receiver_ip2, receiver_port2))
server_sock2.listen(1)

print(f"Waiting for a connection on {receiver_ip2}:{receiver_port2}")

connection2, sender_address2 = server_sock2.accept()
print(f"Connection established with {sender_address2}")


def generate_dummy_data():
    with open('./saving/science_data.txt', 'w', newline='') as txtfile:
        # with open('./saving/science_data.csv', 'w', newline='') as csvfile:
        header_row = "Temperature\tPressure\tHumidity\tAltitude\tMethane\tTVOC\tCO2\tCO\tO2\tNH3\tH2S\tNO2\tSO2\tO3\tCl2\tAS726x_S1\tAS726x_S2\tAS726x_S3\tAS726x_S4\tAS726x_S5\tAS726x_S6\tCarson_Value\tSoil_Temperature\tSoil_Moisture\tSoil_pH\n"
        txtfile.write(header_row)
        # csvfile.write(header_row)
    # count = 0
        while True:
            # print('hi')
            data3 = connection1.recv(1024).decode('utf-8')
            # print(data3)
            # gps = "10,20,30"
            # count = count +1
            # print(count)
            # if(count<10):
            # data3 ="S676.51,876.66,714.08,858.39,788.23,736.20M0.00T24.44P16.19EZC110M110O0F400T33.00P1006.00H67.40DSX"
            # else:
            #     data3 ="S676.51,876.66,714.08,858.39,788.23,736.20M0.0Z0T24.44P16.19EZC110M110O0F400T33.00P1006.00H67.40DSX"
            try:
                data1, data2 = data3.split('Z')
            except:
                continue
            # gps = connection2.recv(1024).decode('utf-8')
            # lat,lon,alt = gps.split(',')
            # print(gps)
            # C438M438O41F446T33.39P1003.59H62.42DSEX
            
            
            try:
                # if 'S' in data1 and 'M' in data1 and 'T' in data1 and 'P' in data1 and 'E' in data1 and 'M' in data2 and 'O' in data2 and 'F' in data2 and 'T' in data2 and 'P' in data2 and 'H' in data2 and 'O' in data2 and data2.endswith('X'):
                combine1 = data1[1:-1].replace('M', ',').replace('T', ',').replace('P', ',')
                spec1, spec2, spec3, spec4, spec5, spec6, moistmeter, temp, pHahaha = combine1.split(',')
                combine2 = data2[1:-1].replace('M', ',').replace('H', ',').replace('P', ',').replace('T', ',').replace('O', ',').replace('F', ',').replace('D', ',')
                coo, meth, tvoc, co2, temp1, pres, hum, dir = combine2.split(',')
                print(f"Received data: {combine1}")
                print(f"Received data: {combine2}")
                # else:
                #     print("invalid data")
            except:
                continue

                # # time.sleep(700)
                # # Generate dummy data for each sensor
                # bme688_data = {
                #     'temperature': round(random.uniform(31, 35),2),
                #     'pressure': round(random.uniform(999.46, 1054),2),
                #     'humidity': round(random.uniform(79.32, 86),2),
                #     'altitude': round(random.uniform(0,115.37),2),
                # }

                # mq4_data = {
                #     'methane': round(random.uniform(254, 255), 2),
                # }

                # sgp30_data = {
                #     'tvoc': round(random.uniform(0,20), 2),
                #     'co2': round(random.uniform(400, 430), 2),
                # }

                # ze03_data = {
                #     'co': round(random.uniform(0, 20), 2),
                #     'o2': round(random.uniform(19, 21), 2),
                #     'nh3': round(random.uniform(50, 60), 2),
                #     'h2s': round(random.uniform(10, 20), 2),
                #     'no2': round(random.uniform(20, 30), 2),
                #     'so2': round(random.uniform(30, 40), 2),
                #     'o3': round(random.uniform(10, 20), 2),
                #     'cl2': round(random.uniform(0, 10), 2),
                # }

                # as726x_data = {
                #     # Dummy data for AS726x sensor
                # }

                # carson_data = {
                #     # Dummy data for Carson microscope
                # }

                # soil_probe_data = {
                #     'temperature': round(random.uniform(24, 26), 2),
                #     'moisture': round(random.uniform(13, 17), 2),
                #     'ph_value': round(random.uniform(6, 8), 2),
                    
                # }
                # # print("HI")
            csv_row = (
                f"{temp1}\t\t"
                f"{pres}\t\t"
                f"{hum}\t\t"
                f"0\t\t"
                f"{meth}\t\t"
                f"{tvoc}\t\t"
                f"{co2}\t\t"
                f"{coo}\t\t"
                f"0\t\t"
                f"{dir}\t\t"
                f"-\t\t"
                f"-\t\t"
                f"-\t\t"
                f"-\t\t"
                f"-\t\t"
                f"{spec1}\t\t"
                f"{spec2}\t\t"
                f"{spec3}\t\t"
                f"{spec4}\t\t"
                f"{spec5}\t\t"
                f"{spec6}\t\t"
                f"-\t\t"
                f"{temp}\t\t"
                f"{moistmeter}\t\t"
                f"{pHahaha}\n"
            )

            # # Write the CSV row to the file
            txtfile.write(csv_row)
            txtfile.flush()
            # csvfile.write(csv_row)
            # csvfile.flush()

            data = {
                'bme688':
                {
                    'temperature': temp1,
                    'pressure': pres,
                    'humidity': hum,
                    'altitude': "wooo",
                },
                'mq4': 
                {
                    'methane': meth,
                },
                'sgp30': 
                {
                    'tvoc': tvoc,
                    'co2': co2,
                },
                'ze03': 
                {
                    'co': coo,
                    'o2': lat,
                    'nh3': lon,
                    'h2s': dir,


                },
                'as726x': {
                    # 's1':round(random.uniform(200, 600), 2),
                    # 's2':round(random.uniform(200, 600), 2),
                    # 's3':round(random.uniform(200, 600), 2),
                    # 's4':round(random.uniform(200, 600), 2),
                    # 's5':round(random.uniform(200, 600), 2),
                    # 's6':round(random.uniform(200, 600), 2),
                    's1':spec1,
                    's2':spec2,
                    's3':spec3,
                    's4':spec4,
                    's5':spec5,
                    's6':spec6,
                    },
                # 'carson': carson_data,
                'soil_probe': 
                
                {
                    'temperature': temp,
                    'moisture': moistmeter,
                    'ph_value': pHahaha,  
                },
            }
            # Emit dummy data to the Flask app
            sio.emit('update_data', data)
            # print(data)
            time.sleep(1)


        # data1 = connection.recv(1024).decode('utf-8')
        # data2 = connection.recv(1024).decode('utf-8')
        # data1="S1.45,2.19,4.46,5.93,8.35,8.78M0.00T31.44P6.73E"
        # if 'S' in data1 and 'M' in data1 and 'T' in data1 and 'P' in data1 and 'E' in data1:
        #     combine = data1[1:-1].replace('M',',').replace('T',',').replace('P',',')
        #     spec1,spec2,spec3,spec4,spec5,spec6,moistmeter,temp,pH = combine.split(',')
        #     print(f"Received data: {combine}")
        # else:
        #     print("invalid data")

# except KeyboardInterrupt:
#     connection.close()
#     server_sock.close()
#     print("Socket closed.")


# Connect to the Flask app
@sio.on('connect')
def on_connect():
    print('Connected to Flask server')

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from Flask server')


def ros_image_callback(data):
    print("Real")
    # Convert ROS Image to OpenCV format
    cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

    # Encode the OpenCV image to JPEG format
    _, img_encoded = cv2.imencode('.jpg', cv_image)

    # Convert the image data to bytes for transmission
    image_bytes = img_encoded.tobytes()

    # Send the image data to connected clients through Socket.IO
    socketio.emit('camera_feed', {'image': True, 'buffer': image_bytes})
    



# def generate_bme_data():
#     return {
#         'temperature': random.uniform(31, 35),
#         'pressure': random.uniform(999.46, 1054),
#         'humidity': random.uni form(79.32, 86),
#         'altitude': random.uniform(0,115.37),
#     }

# def generate_mq4_data():
#     return {
#         'methane': random.uniform(254, 255),
#     }

# def generate_sgp30_data():
#     return{
#         'tvoc': random.uniform(0,20),
#         'co2': random.uniform(400, 430),
#     }

# def generate_ze03_data():
#     return{
#         'co': random.uniform(20,40),
#         'o2': random.uniform(19,21),
#         'nh3': random.uniform(50,60),
#         'h2s': random.uniform(10,20),
#         'no2': random.uniform(20,30),
#         'so2': random.uniform(30,40),
#         'o3': random.uniform(10,20),
#         'cl2': random.uniform(0,10),
#     }

# def generate_soil_data():
#     return{
#         'temp': random.uniform(24,26),
#         'moisture': random.uniform(13,17),
#         'pH': random.uniform(6,8),
#     }


# def emit_dummy_data():
#     while True:
#         dummy_data = {
#             'bme688': generate_bme_data(),
#             'mq4': generate_mq4_data(),
#             'sgp30': generate_sgp30_data(),
#             'zeo3': generate_ze03_data(),
#             'soil': generate_soil_data(),
#         }

#         socketio.emit('sensor_data', dummy_data)
#         time.sleep(1)  # Adjust the sleep duration as needed
plt.ion()  

fig, ax = plt.subplots()
coordinates = []
moving = False  

def plot_live_coordinates(ax, coordinates, moving):
    ax.clear()
    if moving:
        ax.plot(*zip(*coordinates), marker='o', color='red')
    else:
        ax.plot(*zip(*coordinates), marker='o', color='red', linestyle='--')
    ax.set_title('Live Incrementing Coordinates')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

def decimal_diff(coord1, coord2):
    decimal_places = 5
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return (
        Decimal(lat1).quantize(Decimal('1e-{0}'.format(decimal_places))) !=
        Decimal(lat2).quantize(Decimal('1e-{0}'.format(decimal_places))) or
        Decimal(lon1).quantize(Decimal('1e-{0}'.format(decimal_places))) !=
        Decimal(lon2).quantize(Decimal('1e-{0}'.format(decimal_places)))
    )
def gps_reader():
    global coordinates, moving, lat, lon
    last_coordinate = None

    while True:
        try:
            gps = connection2.recv(1024).decode('utf-8')
            # gps = "10.0, 20.0, 30.0"
            lat,lon,alt = gps.split(',')
            new_coordinate = (lat, lon) 
            print("gps updated to: ", new_coordinate)

            if last_coordinate and decimal_diff(last_coordinate, new_coordinate):
                coordinates.append(new_coordinate)
                moving = True
            elif not last_coordinate:
                coordinates.append(new_coordinate)

            last_coordinate = new_coordinate

            time.sleep(1)  
        except Exception as e:
            print(f"error gps: {e}")


if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    # generate_dummy_data()
    # Start a new thread for the dummy data generator
    dummy_data_thread = threading.Thread(target=generate_dummy_data)
    dummy_data_thread.start()
    print("started")
    gps_thread = threading.Thread(target=gps_reader, daemon=True)
    gps_thread.start()

def update(frame):
    global coordinates, moving
    plot_live_coordinates(ax, coordinates, moving)
    plt.draw()  
    moving = False  

ani = FuncAnimation(fig, update, blit=False, interval=3000)  

plt.show(block=True)  
    # rospy.init_node('ros_socketio_camera_server', anonymous=True)
    # rospy.Subscriber('/usb_cam/image_raw', Image, ros_image_callback)   


    # Keep the main script running
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
        #     sio.disconnect()



# # dummy_data_generator.py
# from flask import Flask, render_template, Response
# import socketio
# import random
# import time
# from flask_socketio import SocketIO
# from sensor_msgs.msg import Image   
# from cv_bridge import CvBridge
# import rospy
# import threading
# import socket
# import cv2
# import pickle

# # app = Flask(__name__)
# receiver_ip = ''
# receiver_port1 = 12345
# sio = socketio.Client()
# bridge = CvBridge()

# # receiver_ip2=''
# # receiver_port2 = 5005

# # app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


# server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_sock.bind((receiver_ip, receiver_port1))
# server_sock.listen(1)

# print(f"Waiting for a connection on {receiver_ip}:{receiver_port1}")

# connection, sender_address = server_sock.accept()
# print(f"Connection established with {sender_address}")

# # server_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # server_sock2.bind((receiver_ip2, receiver_port2))
# # server_sock2.listen(1)
# # print(f"Waiting for a connection on {receiver_ip2}:{receiver_port2}")

# # connection2, sender_address2 = server_sock2.accept()
# # print(f"Connection established with {sender_address2}")
# # C104M104O15E420T33.85P1000.36H62.71E

# def generate_dummy_data():
#     while True:
#         while True:
#             data3 = connection.recv(1024).decode('utf-8')
#             # gps = connection2.recv(1024).decode('utf-8')
#             # print('gps',gps)
#             data1, data2 = data3.split('C')
#             print(data1)
#             print(data2)
#             if 'S' in data1 and 'M' in data1 and 'T' in data1 and 'P' in data1 and 'E' in data1 and 'M' in data2 and 'E' in data2 and 'T' in data2 and 'P' in data2 and 'H' in data2 and 'O' in data2 and data2.endswith('E'):
#                 combine1 = data1[1:-1].replace('M',',').replace('T',',').replace('P',',')
#                 spec1,spec2,spec3,spec4,spec5,spec6,moistmeter,temp,pHahaha = combine1.split(',')
#                 combine2 = data2[0:-1].replace('M',',').replace('H',',').replace('P',',').replace('T',',').replace('E',',').replace('O',',')
#                 coo, meth, tvoc, co2, temp1, pres, hum = combine2.split(',')
#                 print(f"Received data: {combine1}")
#                 print(f"Received data: {combine2}")
                
#             else:
#                 print("invalid data")

#         # # time.sleep(700)
#         # # Generate dummy data for each sensor
#         # bme688_data = {
#         #     'temperature': round(random.uniform(31, 35),2),
#         #     'pressure': round(random.uniform(999.46, 1054),2),
#         #     'humidity': round(random.uniform(79.32, 86),2),
#         #     'altitude': round(random.uniform(0,115.37),2),
#         # }

#         # mq4_data = {
#         #     'methane': round(random.uniform(254, 255), 2),
#         # }

#         # sgp30_data = {
#         #     'tvoc': round(random.uniform(0,20), 2),
#         #     'co2': round(random.uniform(400, 430), 2),
#         # }

#         # ze03_data = {
#         #     'co': round(random.uniform(0, 20), 2),
#         #     'o2': round(random.uniform(19, 21), 2),
#         #     'nh3': round(random.uniform(50, 60), 2),
#         #     'h2s': round(random.uniform(10, 20), 2),
#         #     'no2': round(random.uniform(20, 30), 2),
#         #     'so2': round(random.uniform(30, 40), 2),
#         #     'o3': round(random.uniform(10, 20), 2),
#         #     'cl2': round(random.uniform(0, 10), 2),
#         # }

#         # as726x_data = {
#         #     # Dummy data for AS726x sensor
#         # }

#         # carson_data = {
#         #     # Dummy data for Carson microscope
#         # }

#         # soil_probe_data = {
#         #     'temperature': round(random.uniform(24, 26), 2),
#         #     'moisture': round(random.uniform(13, 17), 2),
#         #     'ph_value': round(random.uniform(6, 8), 2),
            
#         # }
#         # # print("HI")

#         data = {
#             'bme688':
#             {
#                 'temperature': temp1,
#                 'pressure': pres,
#                 'humidity': hum,
#                 'altitude': "wooo",
#             },
#             'mq4': 
#             {
#                 'methane': meth,
#             },
#             'sgp30': 
#             {
#                 'tvoc': tvoc,
#                 'co2': co2,
#             },
#             'ze03': 
#             {
#                 'co': coo,
#                 # 'o2': gps,
#                 'nh3': round(random.uniform(50, 60), 2),
#                 'h2s': round(random.uniform(10, 20), 2),
#                 'no2': round(random.uniform(20, 30), 2),
#                 'so2': round(random.uniform(30, 40), 2),
#                 'o3': round(random.uniform(10, 20), 2),
#                 'cl2': round(random.uniform(0, 10), 2),

#             },
#             'as726x': {
#                 # 's1':round(random.uniform(200, 600), 2),
#                 # 's2':round(random.uniform(200, 600), 2),
#                 # 's3':round(random.uniform(200, 600), 2),
#                 # 's4':round(random.uniform(200, 600), 2),
#                 # 's5':round(random.uniform(200, 600), 2),
#                 # 's6':round(random.uniform(200, 600), 2),
#                 's1':spec1,
#                 's2':spec2,
#                 's3':spec3,
#                 's4':spec4,
#                 's5':spec5,
#                 's6':spec6,
#                 },
#             # 'carson': carson_data,
#             'soil_probe': 
            
#             {
#                 'temperature': temp,
#                 'moisture': moistmeter,
#                 'ph_value': pHahaha,  
#             },
#         }
#         # Emit dummy data to the Flask app
#         sio.emit('update_data', data)
#         # print(data)
#         time.sleep(1)


#         # data1 = connection.recv(1024).decode('utf-8')
#         # data2 = connection.recv(1024).decode('utf-8')
#         # data1="S1.45,2.19,4.46,5.93,8.35,8.78M0.00T31.44P6.73E"
#         # if 'S' in data1 and 'M' in data1 and 'T' in data1 and 'P' in data1 and 'E' in data1:
#         #     combine = data1[1:-1].replace('M',',').replace('T',',').replace('P',',')
#         #     spec1,spec2,spec3,spec4,spec5,spec6,moistmeter,temp,pH = combine.split(',')
#         #     print(f"Received data: {combine}")
#         # else:
#         #     print("invalid data")

# # except KeyboardInterrupt:
# #     connection.close()
# #     server_sock.close()
# #     print("Socket closed.")


# # Connect to the Flask app
# @sio.on('connect')
# def on_connect():
#     print('Connected to Flask server')

# @sio.on('disconnect')
# def on_disconnect():
#     print('Disconnected from Flask server')


# def ros_image_callback(data):
#     print("Real")
#     # Convert ROS Image to OpenCV format
#     cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

#     # Encode the OpenCV image to JPEG format
#     _, img_encoded = cv2.imencode('.jpg', cv_image)

#     # Convert the image data to bytes for transmission
#     image_bytes = img_encoded.tobytes()

#     # Send the image data to connected clients through Socket.IO
#     socketio.emit('camera_feed', {'image': True, 'buffer': image_bytes})
    



# # def generate_bme_data():
# #     return {
# #         'temperature': random.uniform(31, 35),
# #         'pressure': random.uniform(999.46, 1054),
# #         'humidity': random.uni form(79.32, 86),
# #         'altitude': random.uniform(0,115.37),
# #     }

# # def generate_mq4_data():
# #     return {
# #         'methane': random.uniform(254, 255),
# #     }

# # def generate_sgp30_data():
# #     return{
# #         'tvoc': random.uniform(0,20),
# #         'co2': random.uniform(400, 430),
# #     }

# # def generate_ze03_data():
# #     return{
# #         'co': random.uniform(20,40),
# #         'o2': random.uniform(19,21),
# #         'nh3': random.uniform(50,60),
# #         'h2s': random.uniform(10,20),
# #         'no2': random.uniform(20,30),
# #         'so2': random.uniform(30,40),
# #         'o3': random.uniform(10,20),
# #         'cl2': random.uniform(0,10),
# #     }

# # def generate_soil_data():
# #     return{
# #         'temp': random.uniform(24,26),
# #         'moisture': random.uniform(13,17),
# #         'pH': random.uniform(6,8),
# #     }


# # def emit_dummy_data():
# #     while True:
# #         dummy_data = {
# #             'bme688': generate_bme_data(),
# #             'mq4': generate_mq4_data(),
# #             'sgp30': generate_sgp30_data(),
# #             'zeo3': generate_ze03_data(),
# #             'soil': generate_soil_data(),
# #         }

# #         socketio.emit('sensor_data', dummy_data)
# #         time.sleep(1)  # Adjust the sleep duration as needed


# if __name__ == '__main__':
#     sio.connect('http://localhost:5000')

#     # generate_dummy_data()
#     # Start a new thread for the dummy data generator
#     dummy_data_thread = threading.Thread(target=generate_dummy_data)
#     dummy_data_thread.start()
#     print("started")

#     # rospy.init_node('ros_socketio_camera_server', anonymous=True)
#     # rospy.Subscriber('/usb_cam/image_raw', Image, ros_image_callback)   


#     # Keep the main script running
#     # try:
#     #     while True:
#     #         time.sleep(1)
#     # except KeyboardInterrupt:
#         #     sio.disconnect()
