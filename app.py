from flask import Flask, render_template, request, redirect
from utils import *
from bokeh.embed import components
from bokeh.util.string import encode_utf8
import logging
import gunicorn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/dashboard')


@app.route('/dashboard')
def index():
    df = get_data()
    logger.info("Data are loaded"+str(len(df)))
    q1a = df.vehicle_id.groupby(df.index).count()
    plot = build_chart(q1a)
    script1, div1 = components(plot)
    html = render_template('pages/index.html', script1=script1, div1=div1)
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(port=33507)
