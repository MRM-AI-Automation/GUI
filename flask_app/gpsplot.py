import socket
import matplotlib
matplotlib.use('TkAgg')  # Use the TkAgg backend, which is compatible with Windows
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.animation import FuncAnimation

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 12345

server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

while True:
    data = client_socket.recv(1024)
    if not data:
        break
    data = data.decode('utf-8')
    lat,lon,alt = data.split(',')
    print(f"lat = {lat}, lon = {lon}, alt = {alt} m")
    lat = float(lat)
    long = float(lon)
    alt = float(alt)

    def generate_next_coordinate():
        # Use the predefined latitude and longitude variables
        return long, lat

    def plot_live_coordinates(ax, coordinates, labels):
        ax.clear()
        ax.plot(*zip(*coordinates), marker='o', color='red')
        
        for label, coord in zip(labels, coordinates):
            ax.text(coord[0], coord[1], label, fontsize=8, ha='right')
        
        ax.set_title('Live GPS Coordinates')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

    def on_button_click(event):
        labels.append(textbox.text)
        textbox.set_val("")
        new_coordinate = generate_next_coordinate()
        coordinates.append(new_coordinate)

    def update(frame):
        plot_live_coordinates(ax, coordinates, labels)

    fig, ax = plt.subplots()

    # Starting coordinates from the variables
    initial_coordinates = [generate_next_coordinate()]

    coordinates = initial_coordinates.copy()
    labels = ["Start"]

    plot_live_coordinates(ax, coordinates, labels)

    plt.subplots_adjust(bottom=0.2)
    ax_button = plt.axes([0.7, 0.05, 0.1, 0.075])
    button = Button(ax_button, 'Label', color='lightgoldenrodyellow', hovercolor='0.975')

    textbox_ax = plt.axes([0.1, 0.05, 0.5, 0.075])
    plt.text(0.03, 0.5, 'Label:', transform=fig.transFigure, fontsize=10, verticalalignment='center')
    textbox = TextBox(textbox_ax, 'Label', initial="")

    button.on_clicked(on_button_click)

    ani = FuncAnimation(fig, update, blit=False, interval=1000)  # Update every 1000 milliseconds (1 second)

    plt.show()


client_socket.close()
server_socket.close()