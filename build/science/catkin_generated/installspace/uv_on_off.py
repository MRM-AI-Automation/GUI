import serial
import threading
import time

state = 1
serial_port = "/dev/ttyUSB1"  # Change this to your Arduino's serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

def send_serial_data():
    global state
    while True:
        ser.write(str(state).encode())  # Send the state data
        time.sleep(1)  # Adjust the delay as needed

sender_thread = threading.Thread(target=send_serial_data)
sender_thread.start()

while True:
    user_input = input("Enter '1' or '0' to change state, or 'q' to quit: ")
    if user_input == "q":
        break
    elif user_input == "1":
        state = 1
    elif user_input == "0":
        state = 0
    else:
        print("Invalid input! Please enter '1', '0', or 'q'.")

sender_thread.join()  # Wait for the sender thread to finish
ser.close()  # Close the serial port
