import socket

# define connection host and port
# here, we still cannot connect with other pc of different IP Address
# due to the limit of python socket
# so, loop back address is used
HOST = 'localhost'
PORT = 65432


# format any data as string, then encode and send to server
def send(conn, data):
    if type(data) != type(''):
        data = str(data).strip()
    conn.sendall(data.encode('utf8'))


# receive byte-like data from, then decode and return it
def receive(conn):
    return conn.recv(1024).decode('utf8').strip()


# try to establish between client side and server side
# through provided socket object passed as parameter
def connecting_stage(sio):
    while True:
        # tie HOST and PORT of connection
        server_address = (HOST, PORT)
        # try to connect with socket server,
        # in case the connection is succeed, then move to next stage
        try:
            sio.connect(server_address)
            break
        # in case errors occurs, display msg and try to connect another time
        except Exception:
            print('There is an issue while connecting.',
                  str(Exception))


# display the main menu, evaluate and return user's choice
def welcome_option():
    INSTRUCTION = '''
    0. Shut down server
    1. View available rooms
    2. View reserved rooms
    3. View occupied rooms
    4. Reserve a room
    5. Occupy a room
    '''
    # print the menu
    print(INSTRUCTION)
    # as user inputs the choice, evaluate the choice
    while True:
        option = int(input('Your choice: '))
        # identify if the input choice is valid
        if option in range(0, 6):
            return option
        else:
            print('Invalid choice')


# handle room reserving as user's choice
def reserve(sio):
    # as the server sends the msg as a list-like string
    # eval() function will turn msg into list
    # then turn into comma-seperated string to display
    available_rooms = ', '.join(eval(receive(sio)))
    print('Available rooms:', available_rooms)
    # ask for user choice for the room id can be reserved
    room_choice = input('Type room id you want to occupy: ')
    # evaluate user choice
    # if a valid choice is made, send to server and prompt success msg
    if room_choice in available_rooms:
        send(sio, room_choice)
        print('Operation succeed')
    # or else, raise error msg
    else:
        print('Error: Room must be available!')


def occupy(sio):
    # as the server sends the msg as a list-like string
    # eval() function will turn msg into list
    # then turn into comma-seperated string to display
    available_rooms = ', '.join(eval(receive(sio)))
    reserved_rooms = ', '.join(eval(receive(sio)))
    print('Available rooms:', available_rooms)
    print('Reserved rooms:', reserved_rooms)
    # ask for user choice for the room id can be reserved
    room_choice = input('Type room id you want to occupy: ')
    # evaluate user choice
    # if a valid choice is made, send to server and prompt success msg
    if room_choice in available_rooms or room_choice in reserved_rooms:
        send(sio, room_choice)
        print('Operation succeed')
    # or else, raise error msg
    else:
        print('Error: Room must be available or reserved!')


# initalize an IPV4 TCP socket instance
sio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 'option' represents user choice in menu
option = -1

# establish connection
connecting_stage(sio)

# prompt the menu, then store user's choice in 'option'
send(sio, option)
# user's choice to socket
option = welcome_option()

# in this case, display list of rooms with specific status
if option in range(1, 4):
    print(receive(sio))
# in this case, reserve a room
elif option == 4:
    reserve(sio)
# in this case, occupy a room
elif option == 5:
    occupy(sio)
# as the user's input is not valid, close connection
else:
    sio.close()
