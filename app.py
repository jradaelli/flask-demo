from flask import Flask, render_template, redirect
from bokeh.embed import components

from plots import *
from bokeh.util.string import encode_utf8
# import gunicorn
import datetime as dt


app = Flask(__name__)

global df
df = get_data1()


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/question1')
def render_q1a(df=df):
    # mask = ((df.index >= pd.datetime(2015, 9, 17, 9, 0)) &
    #         (df.index < pd.datetime(2015, 9, 17, 12, 0)))
    # df = df.loc[mask]
    q1a = df.vehicle_id.groupby(df.index).count()
    plot = build_q1a(q1a)
    plot2 = build_q1b(df)
    script, div = components(plot)
    script2, div2 = components(plot2)
    html = render_template('graph.html', script=script, div=div,
                           script2=script2, div2=div2,
                           title='Plot Some Data')
    return encode_utf8(html)


@app.route('/question2')
def render_q12(df=df):
    plot1 = build_q1b(df)
    number = build_q2a(df)
    plot2 = build_q2b(df)
    script1, div1 = components(plot1)
    script2, div2 = components(plot2)
    surveydt = dt.datetime.utcnow() - dt.timedelta(hours=4)
    surveydt = surveydt.strftime("%Y-%m-%d %H:%M:%S")
    html = render_template('graph2.html', script1=script1, div1=div1,
                           script2=script2, div2=div2,
                           counter=number, surveydt=surveydt,
                           title='Integrating Live Data')
    return encode_utf8(html)


if __name__ == '__main__':
    app.run(port=33507)
