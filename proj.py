from numpy import *
from bokeh.io import curdoc, show
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import *
from bokeh.embed import file_html, components
from bokeh.resources import CDN

g = -9.81
h = 0.0
vi = 5
theta = deg2rad(45)
viy = vi * cos(theta)
vix = vi * sin(theta)
t_start = 0.0


def vrtx(a, b, c):
    return -b/(2*a) + c


def gravity(x):
    x = x - t_start
    result = ((g / 2) * (x ** 2)) + (viy * x) + h
    return result


max_h = gravity(vrtx(g / 2, viy, t_start))
t_impact = roots([g / 2, viy, h])[0] + t_start
x_cords = arange(t_start, t_impact, (t_impact-t_start)/3000)
y_cords = [gravity(x) for x in x_cords]
grav_source = ColumnDataSource(data=dict(x=x_cords, y=y_cords))

# Creates figure object to reference
grav = figure()
# Draws line
grav.line('x', 'y', source=grav_source)
# Places axis labels
grav.xaxis.axis_label = 'Time (s)'
grav.yaxis.axis_label = 'Height (m)'
# grav.yaxis.bounds = [0, inf]

grav_panel = Panel(child=grav, title="Gravity")


def projectile(x):
    if isclose(theta, pi/2):
        return 0
    return (tan(theta)*x) + (g*(x**2))/(2*(vi**2)*(cos(theta)**2)) + h


p_impact = roots([g/(2*vi**2*cos(theta)**2), tan(theta), h])[0]
x_cords = arange(0, p_impact, p_impact/3000)
y_cords = [projectile(x) for x in x_cords]
proj_source = ColumnDataSource(data=dict(x=x_cords, y=y_cords))

proj = figure()
proj.line('x', 'y', source=proj_source)
proj.xaxis.axis_label = "X-Position (m)"
proj.yaxis.axis_label = "Height (m)"
# proj.match_aspect = True
# proj.aspect_scale = True
# print(proj.y)
# proj.y_scale = sin(theta)

proj_panel = Panel(child=proj, title="Projectile Motion")


vi_text = TextInput(title="Initial Velocity", value=f"{vi}")
theta_text = TextInput(title="Launch Angle (degrees)", value=f"{round(rad2deg(theta), 5)}")
h_text = TextInput(title="Height", value=f"{h}")
tstart_text = TextInput(title="Launch Time", value=f"{t_start}")
vix_text = Div(text=f"X-Velocity: {round(vix, 5)}")
viy_text = Div(text=f"Initial Y-Velocity: {round(viy, 5)}")
t_impact_text = Div(text=f"Impact Time: {round(t_impact, 5)}")
p_impact_text = Div(text=f"Range: {round(p_impact, 5)}")
max_h_text = Div(text=f"Maximum Height: {round(max_h, 5)}")


# TODO: Add functionality so that lines can be added together

def draw_grav():
    global t_impact
    global max_h
    max_h = gravity(vrtx(g / 2, viy, t_start))
    max_h_text.text = f"Maximum Height: {round(max_h, 5)}"
    t_impact = roots([g / 2, viy, h])[0] + t_start
    t_impact_text.text = f"Impact Time: {round(t_impact, 5)}"
    grav_x = arange(t_start, t_impact, (t_impact-t_start)/3000)
    grav_y = [gravity(x) for x in grav_x]
    grav_source.data = dict(x=grav_x, y=grav_y)


def draw_proj():
    global p_impact
    p_impact = roots([g/(2*vi**2*cos(theta)**2), tan(theta), h])[0]
    p_impact_text.text = f"Range: {round(p_impact, 5)}"
    proj_x = arange(0, p_impact, p_impact/3000)
    proj_y = [projectile(x) for x in proj_x]
    proj_source.data = dict(x=proj_x, y=proj_y)


def all_update(attrname, old, new):
    global vi
    global theta
    global h
    global t_start
    global vix
    global viy
    vi = float(vi_text.value)
    theta = radians(float(theta_text.value))
    h = float(h_text.value)
    t_start = float(tstart_text.value)


def h_update(attrname, old, new):
    all_update("", "", "")
    draw_grav()
    draw_proj()


for w in [h_text, tstart_text]:
    w.on_change('value', h_update)


def vi_update(attrname, old, new):
    global vix
    global viy
    all_update("", "", "")
    vix = round(vi * cos(theta), 5)
    vix_text.text = f"X-Velocity: {vix}"
    viy = round(vi * sin(theta), 5)
    viy_text.text = f"Initial Y-Velocity: {viy}"
    draw_grav()
    draw_proj()


vi_update_callback = CustomJS(code="""
    var data = source.data;
""")


for w in [vi_text, theta_text]:
    # w.on_change('value', vi_update)
    w.js_on_change('value', vi_update_callback)


widgets = column(vi_text, theta_text, h_text, tstart_text, vix_text, viy_text, t_impact_text, p_impact_text, max_h_text)

tabs = Tabs(tabs=[grav_panel, proj_panel])

main_row = row(widgets, tabs)

curdoc().add_root(main_row)