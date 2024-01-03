from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
from flask_cors import CORS 
import socket
import time

last_m1_press_time = 0
last_m2_press_time = 0

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for all origins

# Add the CORS middleware to your Flask app
CORS(app)
ROVER_HOST = "10.0.0.11"
ROVER_PORT = 5005

rover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

gear = 0

@app.route('/')
def index():
    return render_template('controller.html')

def map(value, fromLow, fromHigh, toLow, toHigh):
    # Calculate the scaled value
    scaled_value = (value - fromLow) * (toHigh - toLow) / \
        (fromHigh - fromLow) + toLow
    # Return the scaled value
    return round(scaled_value)


@socketio.on('gamepad_event')
def handle_gamepad_event(data):
    global gear
    global last_m1_press_time
    global last_m2_press_time

    pairs = data.split()

    # Create a dictionary to store the values
    variables = {}
    # print('Pairs:', pairs)

    # Iterate over pairs and update the dictionary
    for pair in pairs:
        # print(pair)
        # Split each pair into key and value
        
        key = pair[0:2]
        value = pair[2:]
        # print(value)
        variables[key] = float(value) if '.' in value else int(value)
    
    # print(variables)
    m1_value = int(variables.get('M1', 100))
    m2_value = int(variables.get('M2', 100))
    x1_value = map(variables.get('X1',0), -1, 1, -1023-100, 1023+100)
    y1_value = map(variables.get('Y1',0), -1, 1, -1023, 1023)
    x2_value = map(variables.get('P1',0), -0.9, 0.9, 10, -10)
    y2_value = map(variables.get('Q1',0), -0.9, 0.9, -10, 10)
    A_value = int(variables.get('A1',0))
    B_value = int(variables.get('A2',0))
    X_value = int(variables.get('A3',0))
    Y_value = int(variables.get('A4',0))
    DpadX_value = int(variables.get('A5',0))
    DpadY_value = int(variables.get('A6',0))
    LT_value = map(variables.get('S1',0), -1, 1, 0, -10)
    RT_value = map(variables.get('S2',0), -1, 1, 0, 10)
    dpad_left = int(variables.get('A5',0))
    aa_value = int(variables.get('A9',0))
    D_value = int(variables.get('D1',0))
    reset_value = int(dpad_left == -1)
    S_value = 0
    a_value = 0

    if A_value == 1:
        a_value = 1
    elif B_value == 1:
        a_value = 2
    elif X_value == 1:
        a_value = 3
    elif Y_value == 1:
        a_value = 4
    elif DpadY_value == 1:
        a_value = 5
    elif DpadY_value == -1:
        a_value = 6
    elif DpadX_value == 1:
        a_value = 7
    else:
        a_value = aa_value

    if LT_value < 0:
        S_value = LT_value
    elif RT_value > 0:
        S_value = RT_value

    # print(LT_value)
    # print(RT_value)
    # print(reset_value)
    # print(y1_value)
    # m1_pressed = False
    # m2_pressed = False
    print(f'M{gear}X{x1_value}Y{y1_value}P{x2_value}Q{y2_value}A{a_value}S{S_value}R{reset_value}D{D_value}E')
    
    m1_prev_state = 0
    m2_prev_state = 0
    debounce_time = 0.5

    if m1_value == 1 and m1_prev_state == 0 and (time.time() - last_m1_press_time) > debounce_time:
        # print("M1 is pressed")
        m1_prev_state = m1_value
        m2_prev_state = m2_value
        last_m1_press_time = time.time()
        time.sleep(0.2)
        gear -= 1

    # Implement debouncing for M2
    if m2_value == 1 and m2_prev_state == 0 and (time.time() - last_m2_press_time) > debounce_time:
        # print("M2 is pressed")
        m1_prev_state = m1_value
        m2_prev_state = m2_value
        last_m2_press_time = time.time()
        time.sleep(0.2)

        gear += 1

    # print(variables)

    rover_socket.sendto(data.encode(), (ROVER_HOST, ROVER_PORT))

    # print('Received gamepad event:', data)
    # print(gear)

if __name__ == '__main__':
    app.run(debug=True)
