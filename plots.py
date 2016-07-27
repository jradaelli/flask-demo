from bokeh.plotting import *
import pandas as pd
import os
from bokeh.charts import Bar
import requests
from bokeh.charts import BoxPlot


def _flatten_dict(root_key, nested_dict, flattened_dict):
    for key, value in nested_dict.iteritems():
        next_key = root_key + "_" + key if root_key != "" else key
        if isinstance(value, dict):
            _flatten_dict(next_key, value, flattened_dict)
        else:
            flattened_dict[next_key] = value
    return flattened_dict


def nyc_current():
    parameters = {'key': 'c6bdf3a7-b571-4f9a-8892-85528b0ae48f'}
    MTA_API_BASE = """http://api.prod.obanyc.com/api/siri/
    vehicle-monitoring.json"""
    resp = requests.get(MTA_API_BASE, params=parameters).json()
    info = resp['Siri']['ServiceDelivery'][
        'VehicleMonitoringDelivery'][0]['VehicleActivity']
    return pd.DataFrame([_flatten_dict('', i, {}) for i in info])


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
    plot = figure(x_axis_type="datetime", width=1250, height=300,
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


def build_q2a(df):
    df_rt = nyc_current()
    routes = pd.DataFrame(df.route_id.unique())
    final_df = df_rt.merge(routes,
                           left_on="MonitoredVehicleJourney_PublishedLineName",
                           right_on=0, how='inner')
    return len(final_df)


def build_q2b(df):
    df['hours'] = df.index.hour
    df = df.groupby(['service_date', 'hours', 'route_id'],
                    as_index=False)['vehicle_id'].count()
    df = df.groupby(['hours', 'route_id'], as_index=False).mean()[
        ['route_id', 'vehicle_id']]
    p = BoxPlot(df, values='vehicle_id', width=1250, height=500,
                label='route_id', title="Route ID",
                color='#001a4d', ylabel='Number of Vehicle',
                legend=None)
    return p
