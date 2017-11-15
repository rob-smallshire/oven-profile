import csv

import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from math import floor, ceil


def plot_command(file_path):
    with open(file_path, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows = []
        for row in csv_reader:
            fields = (int(row[0]),
                      int(row[1]),
                      float(row[2]),
                      int(row[3]),
                      int(row[4]),
                      float(row[5]),
                      float(row[6]))
            print(fields)
            rows.append(fields)

    columns = list(zip(*rows))

    time = [t / 1000 for t in columns[0]]
    status = columns[1]
    temperature_enclosure = columns[5]
    temperature_board = columns[6]

    status_runs = find_runs(status)

    temperature_steps_enclosure, duration_above_temperature_enclosure = cumulative_x_above_y(time, temperature_enclosure, dy=1.0)
    temperature_steps_board, duration_above_temperature_board = cumulative_x_above_y(time, temperature_board, dy=1.0)


    output_file("log_lines.html")

    time_temperature_figure = figure(
        tools="crosshair,pan,box_zoom,reset,save",
        title="Reflow Profile",
        x_axis_label='Elapsed Time (s)',
        y_axis_label='Temperature (°C)'
    )



    time_temperature_figure.line(time, temperature_enclosure, legend='T-enclosure', line_color='red')
    time_temperature_figure.line(time, temperature_board, legend='T-board', line_color='green')


    duration_above_temperature_figure = figure(
        tools="pan,box_zoom,reset,save",
        title="Duration Above Temperature",
        x_axis_label='Duration (s)',
        y_axis_label='Temperature (°C)'
    )

    duration_above_temperature_figure.line(duration_above_temperature_enclosure, temperature_steps_enclosure, legend='T-enclosure', line_color='red')
    duration_above_temperature_figure.line(duration_above_temperature_board, temperature_steps_board, legend='T-board', line_color='green')


    p = gridplot([[duration_above_temperature_figure, time_temperature_figure]], toolbar_location='right')

    show(p)


def cumulative_x_above_y(xs, ys, dy):
    y_low = min(ys)
    y_high = max(ys)

    # Compute one one that we return, as we're subtracting integrals
    # and we need something to subtract from the first one
    y_start = round_down(y_low, dy) - 1
    y_end = round_up(y_high, dy)
    num_y_steps = int(round((y_end - y_start) / dy))
    y_steps = [y_start + i*dy for i in range(num_y_steps)]
    a_steps = [np.trapz(x=xs, y=[min(y, y_step) for y in ys])
               for y_step in y_steps]
    d_steps = [a_steps[i] - a_steps[i-1] for i in range(1, len(a_steps))]
    return y_steps[1:], d_steps


def round_down(n, d):
    return floor(n / d) * d


def round_up(n, d):
    return ceil(n / d) * d


def find_runs(values):
    """Return a list containing the start and stop indexes of continues runs of values"""

