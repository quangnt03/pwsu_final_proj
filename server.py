import socket
import model
from constants import *

# define connection host and port
# here, we still cannot connect with other pc of different IP Address
# due to the limit of python socket
# so, loop back address is used
HOST = 'localhost'
PORT = 65432


# encode data as byte-like string, then send to client 
def send(conn, data):
    if type(data) != type(''):
        data = str(data).strip()
    conn.sendall(data.encode('utf8'))


# receive data as byte-like string, then return decoded data
def receive(conn):
    return conn.recv(1024).decode('utf8')


# handle every listing requests, meaning that display rooms of different status
def handle_listing_request(conn, option):
    # option sent by client is validated, so validation is not necessary 
    # option 1: display available rooms
    if option == 1:
        response_msg = model.get_available_rooms()
    # option 2: display reserved rooms
    elif option == 2:
        response_msg = model.get_reserved_rooms()
    # option 3: display occupied rooms
    else:
        response_msg = model.rooms[OCCUPIED]
    # response_msg should be a string, so cast the list to string
    if response_msg:
        text_msg = str(response_msg)
    # in case response_msg is an empty, raise a prompt instead
    else:
        text_msg = 'There are no rooms of that type'
    # encode msg as byte-like string, then send back to client
    send(conn, text_msg)

# the function handle reserving request from client
def reserve():
    # send a list of available rooms for client first
    available_rooms = model.get_available_rooms()
    send(conn, available_rooms)
    # receive a room id, then reserve using 'model' utilise
    room_id = receive(conn)
    model.reserve(room_id)


# the function handle occuping request from client
def occupy():
    # send a list of available/reserved rooms for client first
    available_rooms = model.get_available_rooms()
    reserved_rooms = model.get_reserved_rooms()
    send(conn, available_rooms)
    send(conn, reserved_rooms)
    # receive a room id, then occupy using 'model' utilise
    room_id = receive(conn)
    model.occupy(room_id)


# get data from presistent memory to three lists of rooms 
# with different status
model.read_file(FILEPATH)

# establish TCP IPV4 socket
# this implementation is more convinent, as it is not essential
# to manully close socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sio:
    # tie HOST and PORT
    sio.bind((HOST, PORT))
    while True:
        # wait for new connection
        # note that sio.listen is block method, so console/terminal would freeze
        sio.listen()
        # accept a new connection, then prompt connection address
        conn, addr = sio.accept()
        print(f'Connected with {addr}')
        # while there is stil a connection 
        with conn:
            # receive menu's choice from user in client side
            option = int(receive(conn))
            # if option is 0, then close the connection
            if option == 0:
                conn.close()
            # if option ranges 1 to 3, display room list with specific status
            elif option in range(1, 4):
                handle_listing_request(conn, option)
            else:
                # option is 4, then handle reserve request from client 
                if option == 4:
                    reserve()
                # option is 5, then handle occupy request from client 
                else:
                    occupy()
                # two above options lead to data modification,
                # so model utility will save the change
                model.write_file(FILEPATH)
                