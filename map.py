import turtle
from constants import *

pen_size = 3
size = 50
origin_x = -200
origin_y = 200
x_text_offset = 10
y_text_offset = -30
default_font = ('Arial', 16, 'bold')


def create_turtle(main_window):
    return turtle.RawTurtle(main_window)


def extract_coordinates(room_id):
    x = int(room_id[-1])
    y = int(room_id[0])
    return (x, y)


def draw_floor(tle, floor):
    x = origin_x + floor + size
    y = origin_y - size * floor * 3 + size * 0.1

    tle.penup()
    tle.goto(x, y)
    tle.pendown()
    tle.write(f'Floor {floor}', font=default_font)

    draw_hallway(tle, floor, x, y)


def draw_hallway(tle, floor, x, y):
    x = x - floor
    y = y - size

    tle.penup()
    tle.goto(x, y)
    tle.pendown()

    y = y - size
    tle.goto(x, y)

    x = size * 4 + x
    tle.goto(x, y)

    y = y + size
    tle.goto(x, y)

    tle.penup()
    tle.goto(x - 2.8 * size, y - size * 0.7)
    tle.pendown()
    tle.write('Hallway', font=default_font)


def draw_room(tle, room_id, status):
    if not room_id or not status:
        pass
    colors = {
        AVAILABLE: 'green',
        RESERVED: 'yellow',
        OCCUPIED: 'red'
    }
    x, y = extract_coordinates(room_id)
    x = origin_x + size * x
    y = origin_y - size * y * 3
    color = colors[status]

    tle.penup()
    tle.goto(x, y)
    tle.pendown()
    tle.fillcolor(color)
    tle.begin_fill()
    for _ in range(4):
        tle.forward(size)
        tle.right(90)
    tle.end_fill()

    tle.penup()
    tle.goto(x + x_text_offset, y + y_text_offset)
    tle.pendown()
    tle.write(room_id, font=default_font)


def init(tle, available_rooms, reserved_rooms, occupied_rooms):
    tle.pensize(pen_size)
    tle.speed(0)

    for i in range(3):
        draw_floor(tle, i + 1)

    for room in available_rooms:
        draw_room(tle, room, AVAILABLE)
    for room in reserved_rooms:
        draw_room(tle, room, RESERVED)
    for room in occupied_rooms:
        draw_room(tle, room, OCCUPIED)
