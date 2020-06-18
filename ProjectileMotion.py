import numpy as np
from numpy import isclose, pi
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.models import TextInput

g = -9.81
h = 0.0
v_iy = 0.0
v_ix = 0.0
v_i = 0.0
t_start = 0.0
theta = 0.0


# Calculates the vertex given a b and c
def vrtx(a, b, c):
    return -b/(2*a) + c


# Helper input function to limit user input
def _input(prompt, in_type):
    # Keeps prompting the user until they give a valid input
    while True:
        try:
            return in_type(input(prompt))
        except:
            print("Non-valid input, try again")


# Gets velocity variables from user
def get_velocity_variables():
    global v_i
    global v_ix
    global v_iy
    global theta
    global h
    # Get v_i
    v_i = _input("Vi: ", float)
    # If v_i is 0 (i.e. unknown) get v_ix and v_iy, otherwise don't bother
    if isclose(v_i, 0):
        v_ix = _input("Vix: ", float)
        v_iy = _input("Viy: ", float)
    # Get launch angle
    theta = np.radians(_input("Theta: ", float))
    # Get launch height
    h = _input("Launch Height: ", float)


# Calculates unknowns from given variables
def calculate_velocity_variables():
    global v_i
    global v_ix
    global v_iy
    # If vi is unknown calculate v_i
    if np.isclose(v_i, 0):
        v_i = round(np.sqrt((v_ix * v_ix) + (v_iy * v_iy)), 8)
    # Calculates v_iy and v_ix using v_i
    v_ix = round(v_i * np.cos(theta), 8)
    v_iy = round(v_i * np.sin(theta), 8)
    print(f"Final values: vi is {v_i}, vix is {v_ix}, viy is {v_iy}")


# Takes a time (x) and calculates the height at that point
def gravity(x):
    x = x - t_start
    result = ((g / 2) * (x ** 2)) + (v_iy * x) + h
    return result


# Creates a gravity graph object
def update_gravity_graph():
    # Limits x_cords to t_start to t_impact
    # + .01 is there so that it doesn't stop prematurely
    # .009 is step value for function
    t_impact = np.roots([g / 2, v_iy, h])[0] + t_start
    x_cords = np.arange(t_start, t_impact + 0.01, 0.009)
    # Loops through x_cords and gets a y value for the function from all of them
    y_cords = [gravity(x) for x in x_cords]

    # Creates figure object to reference
    temp = figure(title="Gravity")

    # Draws line
    temp.line(x=x_cords, y=y_cords)

    # Calculates vertex
    vertex = vrtx(g/2, v_iy, t_start)
    # Places vertex
    temp.circle(vertex, gravity(vertex))
    # Labels axes
    temp.xaxis.axis_label = 'Time (s)'
    temp.yaxis.axis_label = 'Height (m)'
    return temp


# Takes an x-position (x) and calculates the height of that point
def projectile(x):
    if np.isclose(theta, pi/2):
        return h
    return (np.tan(theta)*x) + (g*(x**2))/(2*(v_i**2)*(np.cos(theta)**2)) + h


# Calculates a projectile graph object
def graph_projectile():
    # Limits x_cords to t_start to t_impact
    # + .01 is there so that it doesn't stop prematurely
    # .009 is step value for function
    p_impact = np.roots([g/(2*v_i**2*np.cos(theta)**2), np.tan(theta), h])[0]
    x_cords = np.arange(t_start, p_impact + 0.01, 0.01)
    # Loops through x_cords and gets a y value for the function from all of them
    y_cords = [projectile(x) for x in x_cords]

    # Creates figure object to reference
    temp = figure(title="Projectile", match_aspect=True)

    # Draws line
    temp.line(x=x_cords, y=y_cords)
    # Places vertex
    vertex = vrtx(g/(2*v_i**2*np.cos(theta)**2), np.tan(theta), h)
    temp.circle(vertex, projectile(vertex))
    # Labels axes
    temp.xaxis.axis_label = 'Horizontal Distance (m)'
    temp.yaxis.axis_label = 'Height (m)'
    return temp
# TODO: Add functionality so that user can input which function they want


# get_velocity_variables()
calculate_velocity_variables()

# Creates graph
grav = update_gravity_graph()
# proj = graph_projectile()

graph_column = column(grav)

vi_text = TextInput(title="Initial Velocity", value="0")
theta_text = TextInput(title="Launch Angle (degrees)", value="0")
vix_text = TextInput(title="Initial X-Velocity", value="0")
viy_text = TextInput(title="Initial Y-Velocity", value="0")
h_text = TextInput(title="Height", value="0")
tstart_text = TextInput(title="Launch Time", value="0")


def update_data(attrname, old, new):
    v_i = float(vi_text.value)
    v_ix = float(vix_text.value)
    v_iy = float(viy_text.value)
    theta = float(theta_text.value)
    h = float(h_text.value)
    t_start = float(tstart_text.value)
    if np.isclose(v_i, 0):
        v_i = round(np.sqrt((v_ix * v_ix) + (v_iy * v_iy)), 8)
    # Calculates v_iy and v_ix using v_i
    v_ix = round(v_i * np.cos(theta), 8)
    v_iy = round(v_i * np.sin(theta), 8)
    calculate_velocity_variables()


for w in [vi_text, theta_text, vix_text, viy_text, h_text, tstart_text]:
    w.on_change('value', update_data)

input_column = column(vi_text, theta_text, vix_text, viy_text, h_text, tstart_text)

total_row = row(input_column, graph_column)

# Opens figure in browser
show(total_row)
