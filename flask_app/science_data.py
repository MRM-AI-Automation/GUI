    # dummy_data_generator.py
from flask import Flask, render_template, Response
import socketio
import time
from flask_socketio import SocketIO
from sensor_msgs.msg import Image   
from cv_bridge import CvBridge
import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal
import random


# app = Flask(_name_)
sio = socketio.Client()
bridge = CvBridge()


# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


receiver_ip1 = ''
receiver_port1 = 12348

server_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock1.bind((receiver_ip1, receiver_port1))
server_sock1.listen(1)

print(f"Waiting for a connection on {receiver_ip1}:{receiver_port1}")

connection1, sender_address1 = server_sock1.accept()
print(f"Connection established with {sender_address1}")


def generate_dummy_data():
    with open('/home/siddharth/GUI/flask_app/saving/science_data.txt', 'w', newline='') as txtfile:
        with open('/home/siddharth/GUI/flask_app/saving/science_data.csv', 'w', newline='') as csvfile:
            header_row = "Temperature\tPressure\tHumidity\tMethane\tTVOC\tCO2\tCO\tS1\tS2\tS3\tS4\tS5\tS6\tSoil_Temperature\tSoil_Moisture\tSoil_pH\n"            
            txtfile.write(header_row)
            csvfile.write(header_row)
            while True:
                # print('hi')
                data3 = connection1.recv(1024).decode('utf-8')
                # data3 = "S676.51,876.66,714.08,858.39,788.23,736.20M0.00T24.44EZC110M110O0F400T33.00P1006.00H67.40DSX"
                # data3 = "S676.51,876.66,714.08,858.39,788.23,736.20M5.00T24.44EZC110M110O5F400T33.00P1006.00H67.40DSL69999X13.555B77.055"
                

                # print(data3)
                try:
                    data1,data2 = data3.split('Z')
                    # print("hello")
                    # print(data1)
                    # print(data2)
                except:
                    continue
                # lat, lon = fluctuate_coordinates(fixed_latitude, fixed_longitude)
                try:
                    # if 'S' in data1 and 'M' in data1 and 'T' in data1 and 'P' in data1 and 'E' in data1 and 'M' in data2 and 'O' in data2 and 'F' in data2 and 'T' in data2 and 'P' in data2 and 'H' in data2 and 'O' in data2 and data2.endswith('X'):
                    combine1 = data1[1:-1].replace('M',',').replace('T',',').replace('K',',')
                    # print(f"Received data: {combine1}")
                    spec1, spec2, spec3, spec4, spec5, spec6, moistmeter,temp = combine1.split(',')
                    # print('hi')
                    combine2 = data2[1:-1].replace('M', ',').replace('H', ',').replace('P', ',').replace('T', ',').replace('O', ',').replace('F', ',').replace('D', ',').replace('X', ',').replace('B', ',').replace('L',',')
                    print(f"Received data 2: {combine2}")
                    coo, meth, tvoc, co2, temp1, pres, hum, dir,res,lat,lon = combine2.split(',')
                    # print(f"Received data: {combine1}")
                    # print(f"Received data: {combine2}")
                    # print(lat)
                    # print(dir)
                    cur = 0
                except:
                    continue

                csv_row = (
                    f"{temp1}\t"
                    f"{pres}\t"
                    f"{hum}\t"
                    f"{meth}\t"
                    f"{tvoc}\t"
                    f"{co2}\t"
                    f"{coo}\t"
                    f"{spec1}\t"
                    f"{spec2}\t"
                    f"{spec3}\t"
                    f"{spec4}\t"
                    f"{spec5}\t"
                    f"{spec6}\t"
                    f"{temp}\t"
                    f"{moistmeter}\t"
                    f"{cur}\n"
                    f"{res}\n"
                    f"{dir}\n"
                )

                # # Write the CSV row to the file
                txtfile.write(csv_row)
                txtfile.flush()
                csvfile.write(csv_row)
                csvfile.flush()
                data = {
                    'bme688':
                    {
                        'temperature': temp1,
                        'pressure': pres,
                        'humidity': hum,
                        'altitude': dir,
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
                    },
                    'gps': 
                    {
                        'lat': lat,
                        'lon': lon,
                        'direction': dir,
                    },
                    'as726x': {
                        's1':spec1,
                        's2':spec2,
                        's3':spec3,
                        's4':spec4,
                        's5':spec5,
                        's6':spec6,
                        },
                    'flurometer': 
                    {
                        'cur': cur,  
                        'res': res,
                    },
                    # 'carson': carson_data,
                    'soil_probe': 
                    
                    {
                        'temperature': temp,
                        'moisture': moistmeter,
                    },
                }
                # Emit dummy data to the Flask app
                sio.emit('update_data', data)
                print('Emititng data')
                # print(data)
                time.sleep(1)

# Connect to the Flask app
@sio.on('connect')
def on_connect():
    print('Connected to Flask server')

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from Flask server')


if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    generate_dummy_data()
    # Start a new thread for the dummy data generator
    # dummy_data_thread = threading.Thread(target=generate_dummy_data)
    # dummy_data_thread.start()
    print("started") 
    





