from flask import Flask, render_template, Response
import socketio
import random
import time
from flask_socketio import SocketIO
from sensor_msgs.msg import Image   
from cv_bridge import CvBridge
import threading
import cv2
import csv

sio = socketio.Client()
bridge = CvBridge()

def generate_dummy_data():
    # Open the CSV file for writing
    
    with open('/home/nikhilesh/GUII/flask_app/saving/science_data.txt', 'w', newline='') as txtfile:
        with open('/home/nikhilesh/GUII/flask_app/saving/science_data.csv', 'w', newline='') as csvfile:
            header_row = "Temperature\tPressure\tHumidity\tMethane\tTVOC\tCO2\tCO\tS1\tS2\tS3\tS4\tS5\tS6\tSoil_Temperature\tSoil_Moisture\tSoil_pH\n"            
            txtfile.write(header_row)
            csvfile.write(header_row)

            while True:
                # Generate dummy data for each sensor
                bme688_data = {
                    'temperature': round(random.uniform(31, 35), 2),
                    'pressure': round(random.uniform(999.46, 1054), 2),
                    'humidity': round(random.uniform(79.32, 86), 2),
                    'altitude': round(random.uniform(0, 115.37), 2),
                }

                mq4_data = {
                    'methane': round(random.uniform(254, 255), 2),
                }

                sgp30_data = {
                    'tvoc': round(random.uniform(0, 20), 2),
                    'co2': round(random.uniform(400, 430), 2),
                }

                ze03_data = {
                    'co': round(random.uniform(0, 20), 2),
                    'o2': round(random.uniform(19, 21), 2),
                    'nh3': round(random.uniform(50, 60), 2),
                    'h2s': round(random.uniform(10, 20), 2),
                    'no2': round(random.uniform(20, 30), 2),
                    'so2': round(random.uniform(30, 40), 2),
                    'o3': round(random.uniform(10, 20), 2),
                    'cl2': round(random.uniform(0, 10), 2),
                }

                as726x_data = {
                    's1': random.uniform(0,4000),
                    's2': random.uniform(0,4000),
                    's3': random.uniform(0,4000),
                    's4': random.uniform(0,4000),
                    's5': random.uniform(0,4000),
                    's6': random.uniform(0,4000),
                }

                carson_data = {
                    'Carson_Value': 0,
                }

                soil_probe_data = {
                    'temperature': round(random.uniform(24, 26), 2),
                    'moisture': round(random.uniform(13, 17), 2),
                    'ph_value': round(random.uniform(6, 8), 2),
                }

                # Prepare data for writing to CSV
                csv_row = (
                    f"{bme688_data['temperature']}\t"
                    f"{bme688_data['pressure']}\t"
                    f"{bme688_data['humidity']}\t"
                    f"{mq4_data['methane']}\t"
                    f"{sgp30_data['tvoc']}\t"
                    f"{sgp30_data['co2']}\t"
                    f"{ze03_data['co']}\t"
                    f"{as726x_data['s1']}\t"
                    f"{as726x_data['s2']}\t"
                    f"{as726x_data['s3']}\t"
                    f"{as726x_data['s4']}\t"
                    f"{as726x_data['s5']}\t"
                    f"{as726x_data['s6']}\t"
                    f"{soil_probe_data['temperature']}\t"
                    f"{soil_probe_data['moisture']}\t"
                    f"{soil_probe_data['ph_value']}\n"
                )

                # Write the CSV row to the file
                csvfile.write(csv_row)
                csvfile.flush() 
                txtfile.write(csv_row)
                txtfile.flush()
                 # Ensure the data is written immediately to the file

                # Emit dummy data to the Flask app
                data = {
                    'bme688': bme688_data,
                    'mq4': mq4_data,
                    'sgp30': sgp30_data,
                    'ze03': ze03_data,
                    'as726x': as726x_data,
                    'carson': carson_data,
                    'soil_probe': soil_probe_data,
                }
                sio.emit('update_data', data)
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

    # Start a new thread for the dummy data generator
    dummy_data_thread = threading.Thread(target=generate_dummy_data)
    dummy_data_thread.start()
    print("Started")

    # Keep the main script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sio.disconnect()