import socket
import model
from constants import FILEPATH


def send(conn, data):
    if type(data) != type(''):
        data = str(data).strip()
    conn.sendall(data.encode('utf8'))


def receive(conn):
    return conn.recv(1024).decode('utf8')


def handle_listing_request(conn, option):
    if option == 1:
        response_msg = model.get_available_rooms()
    elif option == 2:
        response_msg = model.get_reserved_rooms()
    else:
        response_msg = model.get_occupied_rooms()
    if response_msg:
        text_msg = ', '.join(response_msg)
    else:
        text_msg = 'There are no rooms of that type'
    send(conn, text_msg)


def reserve():
    available_rooms = model.get_available_rooms()
    send(conn, available_rooms)
    room_id = receive(conn)
    model.reserve(room_id)


def occupy():
    available_rooms = model.get_available_rooms()
    reserved_rooms = model.get_reserved_rooms()
    send(conn, available_rooms)
    send(conn, reserved_rooms)
    room_id = receive(conn)
    model.occupy(room_id)


HOST = '127.0.0.1'
PORT = 65432

model.read_file(FILEPATH)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sio:
    sio.bind((HOST, PORT))
    while True:
        sio.listen()

        conn, addr = sio.accept()
        print(f'Connected with {addr}')

        with conn:
            option = int(receive(conn))
            if option == 0:
                conn.close()
            elif option in range(1, 4):
                handle_listing_request(conn, option)
            else:
                if option == 4:
                    reserve()
                else:
                    occupy()
                model.write_file(FILEPATH)
