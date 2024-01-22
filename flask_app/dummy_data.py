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
    with open('./saving/science_data.txt', 'w', newline='') as csvfile:
        # Write the header row with labels
        header_row = "Temperature\tPressure\tHumidity\tAltitude\tMethane\tTVOC\tCO2\tCO\tO2\tNH3\tH2S\tNO2\tSO2\tO3\tCl2\tAS726x_S1\tAS726x_S2\tAS726x_S3\tAS726x_S4\tAS726x_S5\tAS726x_S6\tCarson_Value\tSoil_Temperature\tSoil_Moisture\tSoil_pH\n"
        csvfile.write(header_row)

        while True:
            # Generate dummy data for each sensor
            bme688_data = {
                'Temperature': round(random.uniform(31, 35), 2),
                'Pressure': round(random.uniform(999.46, 1054), 2),
                'Humidity': round(random.uniform(79.32, 86), 2),
                'Altitude': round(random.uniform(0, 115.37), 2),
            }

            mq4_data = {
                'Methane': round(random.uniform(254, 255), 2),
            }

            sgp30_data = {
                'TVOC': round(random.uniform(0, 20), 2),
                'CO2': round(random.uniform(400, 430), 2),
            }

            ze03_data = {
                'CO': round(random.uniform(0, 20), 2),
                'O2': round(random.uniform(19, 21), 2),
                'NH3': round(random.uniform(50, 60), 2),
                'H2S': round(random.uniform(10, 20), 2),
                'NO2': round(random.uniform(20, 30), 2),
                'SO2': round(random.uniform(30, 40), 2),
                'O3': round(random.uniform(10, 20), 2),
                'Cl2': round(random.uniform(0, 10), 2),
            }

            as726x_data = {
                'AS726x_S1': 0,
                'AS726x_S2': 0,
                'AS726x_S3': 0,
                'AS726x_S4': 0,
                'AS726x_S5': 0,
                'AS726x_S6': 0,
            }

            carson_data = {
                'Carson_Value': 0,
            }

            soil_probe_data = {
                'Soil_Temperature': round(random.uniform(24, 26), 2),
                'Soil_Moisture': round(random.uniform(13, 17), 2),
                'Soil_pH': round(random.uniform(6, 8), 2),
            }

            # Prepare data for writing to CSV
            csv_row = (
                f"{bme688_data['Temperature']}\t\t"
                f"{bme688_data['Pressure']}\t\t"
                f"{bme688_data['Humidity']}\t\t"
                f"{bme688_data['Altitude']}\t\t"
                f"{mq4_data['Methane']}\t\t"
                f"{sgp30_data['TVOC']}\t\t"
                f"{sgp30_data['CO2']}\t\t"
                f"{ze03_data['CO']}\t\t"
                f"{ze03_data['O2']}\t\t"
                f"{ze03_data['NH3']}\t\t"
                f"{ze03_data['H2S']}\t\t"
                f"{ze03_data['NO2']}\t\t"
                f"{ze03_data['SO2']}\t\t"
                f"{ze03_data['O3']}\t\t"
                f"{ze03_data['Cl2']}\t\t"
                f"{as726x_data['AS726x_S1']}\t\t"
                f"{as726x_data['AS726x_S2']}\t\t"
                f"{as726x_data['AS726x_S3']}\t\t"
                f"{as726x_data['AS726x_S4']}\t\t"
                f"{as726x_data['AS726x_S5']}\t\t"
                f"{as726x_data['AS726x_S6']}\t\t"
                f"{carson_data['Carson_Value']}\t\t"
                f"{soil_probe_data['Soil_Temperature']}\t\t"
                f"{soil_probe_data['Soil_Moisture']}\t\t"
                f"{soil_probe_data['Soil_pH']}\n"
            )

            # Write the CSV row to the file
            csvfile.write(csv_row)
            csvfile.flush()  # Ensure the data is written immediately to the file

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