# dummy_data_generator.py
from flask import Flask, render_template, Response
import socketio
import random
import time
from flask_socketio import SocketIO
import threading

sio = socketio.Client()

# Connect to the Flask app
sio.connect('http://localhost:5000')

def generate_dummy_data():
    while True:
        # Generate dummy data for each sensor
        bme688_data = {
            'temperature': round(random.uniform(31, 35),2),
            'pressure': round(random.uniform(999.46, 1054),2),
            'humidity': round(random.uniform(79.32, 86),2),
            'altitude': round(random.uniform(0,115.37),2),
        }

        mq4_data = {
            'methane': round(random.uniform(254, 255), 2),
        }

        sgp30_data = {
            'tvoc': round(random.uniform(0,20), 2),
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
            # Dummy data for AS726x sensor
        }

        carson_data = {
            # Dummy data for Carson microscope
        }

        soil_probe_data = {
            'temperature': round(random.uniform(24, 26), 2),
            'moisture': round(random.uniform(13, 17), 2),
            'ph_value': round(random.uniform(6, 8), 2),
        }

        # Emit dummy data to the Flask app
        sio.emit('sensor_data', {
            'bme688': bme688_data,
            'mq4': mq4_data,
            'sgp30': sgp30_data,
            'ze03': ze03_data,
            'as726x': as726x_data,
            'carson': carson_data,
            'soil_probe': soil_probe_data,
        })

# def generate_bme_data():
#     return {
#         'temperature': random.uniform(31, 35),
#         'pressure': random.uniform(999.46, 1054),
#         'humidity': random.uniform(79.32, 86),
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


if __name__ == '__main__':
    # Start a new thread for the dummy data generator
    dummy_data_thread = threading.Thread(target=generate_dummy_data)
    dummy_data_thread.start()
    print("started")

    # Keep the main script running
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        sio.disconnect()
