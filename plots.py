from bokeh.plotting import *
import pandas as pd
import os
from bokeh.charts import Bar


def date_parser(u):
    date_format_str = "%Y-%m-%d %H:%M:%S"
    return pd.datetime.strptime(u, date_format_str)


def get_data1(date_parser=date_parser):
    root = os.getcwd()
    pathdata = os.path.join(root, "static", "data", "manhattan.csv")

    df = pd.read_csv(pathdata,
                     parse_dates=True,
                     date_parser=date_parser,
                     index_col=1)
    return df


def build_q1a(df):
    x_data = df.index
    y_data = df
    plot = figure(x_axis_type="datetime", width=1400, height=300,
                  tools="pan,xwheel_zoom,box_zoom,reset,resize",
                  title="Vehicle Trend")
    plot.grid.grid_line_alpha = 0.3
    plot.line(x_data, y_data)
    return plot


def build_q1b(df):
    q1b = df.vehicle_id.resample('H').apply(pd.Series.nunique)
    q1b.index = q1b.index.to_series().apply(lambda x: str(
        x).split(' ')[1].replace(':', '-').split("-")[0])
    plot = Bar(q1b, label=q1b.index, agg='mean',
               values='vehicle_id',
               webgl=False, color='navy',
               xlabel="Hours", ylabel="Mean Vehicle",
               title="Vehicle Mean per hour", legend=None)
    return plot
