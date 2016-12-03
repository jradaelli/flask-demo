from bokeh.plotting import *
import pandas as pd
import os


def date_parser(u):
    date_format_str = "%Y-%m-%d %H:%M:%S"
    return pd.datetime.strptime(u, date_format_str)


def get_data(date_parser=date_parser):
    root = os.getcwd()
    pathdata = os.path.join(root, "static", "data", "manhattan.csv")

    df = pd.read_csv(pathdata,
                     parse_dates=True,
                     date_parser=date_parser,
                     index_col=1,
                     nrows=100)
    return df


def build_chart(df):
    x_data = df.index
    y_data = df
    plot = figure(x_axis_type="datetime",
                  tools="pan,xwheel_zoom,box_zoom,reset,resize",
                  title="Vehicle Trend")
    plot.grid.grid_line_alpha = 0.3
    plot.line(x_data, y_data)
    return plot
