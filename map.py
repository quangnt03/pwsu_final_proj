import turtle
from constants import *

# line width of turtle pen
pen_size = 3

# size of each room on the map
size = 50

# set the initial position where turtle pen should be
# else, the pen won't draw in the visible position on parent canvas
origin_x = -150
origin_y = 210

# horizontal & vertical spaces between 'roomid' text and
# the border of room cube
x_text_offset = 10
y_text_offset = -30

# default font style
default_font = ('Arial', 16, 'bold')


# initialize and rawturtle object that can be attached
# in tkinter container component
def create_turtle(main_window):
    return turtle.RawTurtle(main_window)


# get the 'x' and 'y' position of a room based on its id
def extract_coordinates(room_id):
    x = int(room_id[-1])
    y = int(room_id[0])
    return (x, y)


# handle drawing each floor's hallway and floor name
def draw_floor(tle, floor):
    # adjust the turtle pen pos that floor name can be written
    # above the whole floor
    x = origin_x + floor + size
    y = origin_y - size * floor * 3 + size * 0.1
    tle.penup()
    tle.goto(x, y)
    tle.pendown()
    # write the floor name
    tle.write(f'Floor {floor}', font=default_font)
    draw_hallway(tle, floor, x, y)


# handle drawing each floor's hallway
def draw_hallway(tle, floor, x, y):
    # the position where turtle should draw the hallway should
    # be a rooms row far from the 'Floor x' text
    # leave space for a row of rooms
    x = x - floor
    y = y - size
    # set pen position
    tle.penup()
    tle.goto(x, y)
    tle.pendown()
    # start drawing hallway
    y = y - size
    tle.goto(x, y)
    x = size * 4 + x
    tle.goto(x, y)
    y = y + size
    tle.goto(x, y)
    # align 'Hallway' text and write it
    tle.penup()
    tle.goto(x - 2.8 * size, y - size * 0.7)
    tle.pendown()
    tle.write('Hallway', font=default_font)


# drawing single room with provided id and status
def draw_room(tle, room_id, status):
    # if room id is not provided, then the function will not be called
    if not room_id or not status:
        pass
    # define colors for different status of rooms
    colors = {
        AVAILABLE: 'green',
        RESERVED: 'yellow',
        OCCUPIED: 'red'
    }
    # get the coordinate based on room id
    x, y = extract_coordinates(room_id)
    # calculate the proper position to locate turtle pen
    x = origin_x + size * x
    y = origin_y - size * y * 3
    # determine fill color to draw room
    color = colors[status]
    # start drawing and filling the rectangle representing the room
    tle.penup()
    tle.goto(x, y)
    tle.pendown()
    tle.fillcolor(color)
    tle.begin_fill()
    for _ in range(4):
        tle.forward(size)
        tle.right(90)
    tle.end_fill()
    # label the room that was drawn
    tle.penup()
    tle.goto(x + x_text_offset, y + y_text_offset)
    if status != RESERVED:
        tle.color('white')
    tle.pendown()
    tle.write(room_id, font=default_font)
    tle.color('black')


def draw_legend(tle):
    cube_size = 20
    offset = 80
    tle.penup()
    tle.goto(-40, -370)
    tle.pendown()

    tle.fillcolor('red')
    tle.begin_fill()
    for _ in range(4):
        tle.forward(cube_size)
        tle.right(90)
    tle.end_fill()
    tle.write('Occupied', font=('Arial', 13))
    tle.penup()

    tle.forward(offset)
    tle.pendown()
    tle.write('Reserved', font=('Arial', 13))
    tle.fillcolor('yellow')
    tle.begin_fill()
    for _ in range(4):
        tle.forward(cube_size)
        tle.right(90)
    tle.end_fill()

    tle.penup()
    tle.forward(offset)
    tle.pendown()
    tle.write('Available', font=('Arial', 13))
    tle.fillcolor('green')
    tle.begin_fill()
    for _ in range(4):
        tle.forward(cube_size)
        tle.right(90)
    tle.end_fill()

# the init function should be called as the tkinter window starts
# to create a rawturtle instance with given parental components
# also, the function loads three lists of rooms with specific status


def init(tle, available_rooms, reserved_rooms, occupied_rooms):
    tle.pensize(pen_size)
    tle.speed(0)

    draw_legend(tle)

    for i in range(3):
        draw_floor(tle, i + 1)

    for room in available_rooms:
        draw_room(tle, room, AVAILABLE)
    for room in reserved_rooms:
        draw_room(tle, room, RESERVED)
    for room in occupied_rooms:
        draw_room(tle, room, OCCUPIED)
