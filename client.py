import socket

HOST = ''
PORT = 65432


def send(conn, data):
    if type(data) != type(''):
        data = str(data).strip()
    conn.sendall(data.encode('utf8'))


def receive(conn):
    return conn.recv(1024).decode('utf8').strip()


def connecting_stage(sio):
    global HOST
    while True:
        HOST = input('Type host IP: ')
        server_address = (HOST, PORT)
        try:
            sio.connect(server_address)
            break
        except Exception:
            print('There is an issue while connecting.',
                  str(Exception))


def welcome_option():
    INSTRUCTION = '''
    0. Shut down server
    1. View available rooms
    2. View reserved rooms
    3. View occupied rooms
    4. Reserve a room
    5. Occupy a room
    '''
    print(INSTRUCTION)
    while True:
        option = int(input('Your choice: '))
        if option in range(0, 6):
            return option
        else:
            print('Invalid choice')


def reserve(sio):
    available_rooms = ', '.join(eval(receive(sio)))
    print('Available rooms:', available_rooms)
    room_choice = input('Type room id you want to occupy: ')
    if room_choice in available_rooms:
        send(sio, room_choice)
        print('Operation succeed')
    else:
        print('Error: Room must be available!')


def occupy(sio):
    available_rooms = ', '.join(eval(receive(sio)))
    reserved_rooms = ', '.join(eval(receive(sio)))
    print('Available rooms:', available_rooms)
    print('Reserved rooms:', reserved_rooms)

    room_choice = input('Type room id you want to occupy: ')
    if room_choice in available_rooms or room_choice in reserved_rooms:
        send(sio, room_choice)
        print('Operation succeed')
    else:
        print('Error: Room must be available or reserved!')


sio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
option = -1

connecting_stage(sio)

while True:
    option = welcome_option()
    send(sio, option)

    if option in range(1, 4):
        print(receive(sio))
    elif option == 4:
        reserve(sio)
    elif option == 5:
        occupy(sio)
    else:
        sio.close()
        break
