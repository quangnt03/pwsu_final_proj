import csv
from constants import *

# lists of rooms of all statuses
rooms = {
    AVAILABLE: [],
    RESERVED: [],
    OCCUPIED: []
}

# write data to external .csv file with given path
# using for saving data
# data format: room_id,status


def write_file(filepath):
    # declare global rooms lists
    global rooms
    # reach .csv file
    with open(filepath, 'w') as file:
        # write headers
        file.write('room_id,status\n')
        # write rooms id in available list
        for room_id in rooms[AVAILABLE]:
            file.write(f'{room_id},{AVAILABLE}\n')
        # write rooms id in reserved list
        for room_id in rooms[RESERVED]:
            file.write(f'{room_id},{RESERVED}\n')
        # write rooms id in occupied list
        for room_id in rooms[OCCUPIED]:
            file.write(f'{room_id},{OCCUPIED}\n')


# read data from external file with given path
# using for reading saved data
def read_file(filepath):
    # declare global rooms lists
    global rooms
    # reach .csv file
    with open(filepath) as file:
        # create csv reader to read csv-formatted data
        reader = csv.DictReader(file)
        for row in reader:
            rooms[row['status']].append(row['room_id'])


""" Constraints for rooms' status change:
- AVAILABLE -> RESERVED
- AVAILABLE -> OCCUPIED
- RESERVED -> OCCUPIED
- RESERVED -> AVAILABLE
- OCCUPIED -> AVAILABLE
"""
# This function inplements logical constraints for rooms' status change


def change_status(room_id, new_status):
    # declare global rooms lists
    global rooms
    # Set new status to RESERVED
    if new_status == RESERVED:
        # check if the specific room is available rooms
        # if yes, operation is valid
        if room_id in rooms[AVAILABLE]:
            rooms[RESERVED].append(room_id)
            rooms[AVAILABLE].remove(room_id)

    # Set new status to OCCUPIED
    elif new_status == OCCUPIED:
        # check if the specific room is available rooms
        # if yes, operation is valid
        if room_id in rooms[AVAILABLE]:
            rooms[OCCUPIED].append(room_id)
            rooms[AVAILABLE].remove(room_id)
        # check if the specific room is reserved rooms
        # if yes, operation is valid
        elif room_id in rooms[RESERVED]:
            rooms[OCCUPIED].append(room_id)
            rooms[RESERVED].remove(room_id)
    # Set new status to AVAILABLE
    else:
        # check if the specific room is occupied rooms
        # if yes, operation is valid
        if room_id in rooms[OCCUPIED]:
            rooms[AVAILABLE].append(room_id)
            rooms[OCCUPIED].remove(room_id)

        # check if the specific room is reserved rooms
        # if yes, operation is valid
        elif room_id in rooms[RESERVED]:
            rooms[AVAILABLE].append(room_id)
            rooms[RESERVED].remove(room_id)


# This functions changes an available or reserved room with specific 'room_id'
# to 'OCCUPIED' status
def occupy(room_id):
    change_status(room_id, OCCUPIED)


# This functions changes an available room with specific 'room_id'
# to 'RESEREVD' status
def reserve(room_id):
    change_status(room_id, RESERVED)


# This functions changes a reserved or occupied room with specific 'room_id'
# to 'AVAILABLE' status
def make_available(room_id):
    change_status(room_id, AVAILABLE)


# The function returns a list of available rooms
def get_available_rooms():
    return rooms[AVAILABLE]


# The function returns a list of reserved rooms
def get_reserved_rooms():
    return rooms[RESERVED]


# The function returns a list of occupied rooms
def get_occupied_rooms():
    return rooms[OCCUPIED]
