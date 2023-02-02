from tkinter import *
from tkinter import font
from idlelib.tooltip import Hovertip

from constants import *
import model
import map


# When a element in available list is selected
# the function puts the selection in global variable for latter use
# disable reserve button (constraints)
def available_select(event):
    global selection
    selection = list_available.get(ANCHOR)
    btn_free.config(state='disabled')
    btn_reserve.config(state='active')
    btn_occupy.config(state='active')


# When a element in reserved list is selected
# the function puts the selection in global variable for latter use
# disable free button (constraints)
def reserved_select(event):
    global selection
    selection = list_reserved.get(ANCHOR)
    btn_free.config(state='active')
    btn_reserve.config(state='disabled')
    btn_occupy.config(state='active')


# When a element in occupied list is selected
# the function puts the selection in global variable for latter use
# disable reserve and occupy buttons (constraints)
def occupied_select(event):
    global selection
    selection = list_occupied.get(ANCHOR)
    btn_free.config(state='active')
    btn_reserve.config(state='disabled')
    btn_occupy.config(state='disabled')


# update displayed values in three room lists everytime changes occurs
def update_value():
    # the order of rooms in each listbox should be set
    strvar_available.set(sorted(model.get_available_rooms()))
    strvar_reserved.set(sorted(model.get_reserved_rooms()))
    strvar_occupied.set(sorted(model.get_occupied_rooms()))


# disable all buttons and change focus to main window
# when none of rooms is selected
# or after an operation has finished
def set_default_states():
    # disable all button
    btn_free.configure(state='disabled')
    btn_occupy.configure(state='disabled')
    btn_reserve.configure(state='disabled')
    # set root window as the focused component
    window.focus_set()


# occupy a room using model utilitise and update listboxs' value
def occupy():
    # Change the status of the room with 'model module'
    model.occupy(selection)
    # Update the values in three listboxes, as there is a change in
    # room status that affects the values inside listbox
    update_value()
    # Set three operation button to disabled, as now no room is selected
    set_default_states()
    # Redraw the graphical map
    map.draw_room(tle, selection, OCCUPIED)


# reserve a room using model utilitise and update listboxs' value
def reserve():
    # Change the status of the room with 'model module'
    model.reserve(selection)
    # Update the values in three listboxes, as there is a change in
    # room status that affects the values inside listbox
    update_value()
    # Set three operation button to disabled, as now no room is selected
    set_default_states()
    # Redraw the graphical map
    map.draw_room(tle, selection, RESERVED)


# make a room free using model utilitise and update listboxs' value
def free():
    # Change the status of the room with 'model module'
    model.make_available(selection)
    # Update the values in three listboxes, as there is a change in
    # room status that affects the values inside listbox
    update_value()
    # Set three operation button to disabled, as now no room is selected
    set_default_states()
    # Redraw the graphical map
    map.draw_room(tle, selection, AVAILABLE)


# global variables
# when any room from any list is selected, id of the room will be stored
selection = ''

# title and size of main window
title = 'BUV SUNSHINE HOTEL'
window_size = '760x600'

# main window is initialized and set
window = Tk()
window.geometry(window_size)
window.title(title)

# load data from .csv file using model utility
model.read_file(FILEPATH)


# font settings
font_title = font.Font(
    family="Arial",
    size=20,
    weight="bold"
)
font_lb_header = font.Font(
    family="Arial",
    size=14,
    weight="bold"
)
font_lb = font.Font(
    family="Arial",
    size=20
)
font_btn = font.Font(
    family="Arial",
    size=16
)

# create frames containing buttons and listboxes
frm_available = Frame(window)
frm_reserved = Frame(window)
frm_occupied = Frame(window)
cvs_map = Canvas(window)

# app title
Label(text=title, font=font_title).pack(side=TOP, pady=(20, 0))


# create labels for listboxes
lb_available = Label(
    frm_available,
    text='Available',
    font=font_lb_header
)

lb_occupied = Label(
    frm_occupied,
    text='Occupied',
    font=font_lb_header
)

lb_reserved = Label(
    frm_reserved,
    text='Reserved',
    font=font_lb_header
)

# create stringvars that store lines of text representing each room list
strvar_available = StringVar(value=model.get_available_rooms())
strvar_reserved = StringVar(value=model.get_reserved_rooms())
strvar_occupied = StringVar(value=model.get_occupied_rooms())

# listboxes
# listboxes properties
list_width = 6
list_height = 12

# create listbox components to display three lists of rooms
list_available = Listbox(
    frm_available,
    listvariable=strvar_available,
    width=list_width,
    height=list_height,
    font=font_lb
)

list_occupied = Listbox(
    frm_occupied,
    listvariable=strvar_occupied,
    width=list_width,
    height=list_height,
    font=font_lb
)

list_reserved = Listbox(
    frm_reserved,
    listvariable=strvar_reserved,
    width=list_width,
    height=list_height,
    font=font_lb,
)

# create buttons for operations with rooms
btn_free = Button(
    frm_available,
    text='Free',
    command=free,
    font=font_btn,
    width=7
)
btn_occupy = Button(
    frm_occupied,
    text='Occupy',
    command=occupy,
    font=font_btn,
)
btn_reserve = Button(
    frm_reserved,
    text='Reserve',
    command=reserve,
    font=font_btn
)

# hovertip to guide user about operations with selected room
hve_free = Hovertip(btn_free, 'Click to make selected room available')
hve_reserve = Hovertip(btn_reserve, 'Click to reserve selected room')
hve_occupy = Hovertip(btn_occupy, 'Click to occupy selected room')

# create a RawTurtle instance that integrates the hotel
# map in the same window with other widget
tle = map.create_turtle(cvs_map)

# this function is called to disabled all actions buttons
# as no room is initally selected
set_default_states()

# buttons functions bindings
list_available.bind('<ButtonRelease-1>', available_select)
list_reserved.bind('<ButtonRelease-1>', reserved_select)
list_occupied.bind('<ButtonRelease-1>', occupied_select)

# layout/geometry settings
cvs_map.pack(side=LEFT, fill='both')
frm_available.pack(side=LEFT, padx=(25, 15))
frm_reserved.pack(side=LEFT, padx=(10, 25))
frm_occupied.pack(side=LEFT)

lb_available.pack(side=TOP)
list_available.pack(side=TOP, pady=(0, 10))
btn_free.pack(side=TOP)

lb_reserved.pack(side=TOP)
list_reserved.pack(side=TOP, pady=(0, 10))
btn_reserve.pack(side=TOP)

lb_occupied.pack(side=TOP)
list_occupied.pack(side=TOP, pady=(0, 10))
btn_occupy.pack(side=TOP)

# initialize a rawturtle object as the map
# provide lists of stated rooms for drawing graphical map
map.init(
    tle,
    model.get_available_rooms(),
    model.get_reserved_rooms(),
    model.get_occupied_rooms()
)

# main program loop
window.mainloop()

# save data to file as program is closed
model.write_file(FILEPATH)
