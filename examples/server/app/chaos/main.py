from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.models import (Button, ColumnDataSource, Label, Dropdown, Spinner)
from bokeh.plotting import figure

import chaos


# Data
gen = None
source = ColumnDataSource(data={"x": [], "y": []})


def clear_data():
    if button.label != play:
        animate()  # stop animation
    source.data = {"x": [], "y": []}


def get_data():
    points = next(gen)
    data = {"x": points[:, 0],
            "y": points[:, 1]}
    return data


def stream_points():
    source.stream(get_data())


def get_config():
    name = dropdown.label
    config = chaos.configs[name]
    return config


def get_momentum():
    return spinner.value


def init_generator():
    global gen
    config = get_config()
    gen = chaos.generate_chaos(corners=config.corners, momentum=get_momentum())


# controls

def set_config(event):
    name = event.item
    dropdown.label = name
    config = chaos.configs[name]
    spinner.value = config.momentum


confg_names = list(chaos.configs.keys())
dropdown = Dropdown(label=confg_names[0], button_type="default", menu=confg_names, width=100, height=30)
dropdown.on_click(set_config)



def set_momentum(attr, old, new):
    if old == new:
        return
    clear_data()
    spinner.value = round(new, 4)


spinner = Spinner(title="Momentum", low=.01, high=4.0, step=0.04, value=0.5, width=80, height=50)
spinner.on_change("value", set_momentum)



# Animation
play = "► Play"
callback_id = None

def animate():
    global callback_id
    if button.label == play:
        button.label = '❚❚ Pause'
        init_generator()
        callback_id = curdoc().add_periodic_callback(stream_points, 200)
    else:
        button.label = play
        curdoc().remove_periodic_callback(callback_id)

button = Button(label=play, width=80, height=30, sizing_mode="fixed")
button.on_event('button_click', animate)


plot = figure(title="Chaos Theory", sizing_mode="stretch_both")
plot.scatter(source=source, size=2)



# Page layout
layout = layout([
    row([button, dropdown, spinner], sizing_mode="fixed"),
    row([plot]),
], sizing_mode="stretch_both")

curdoc().theme = "dark_minimal"
curdoc().title = "Chaos Theory"
curdoc().add_root(layout)
