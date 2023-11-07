from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import (
    create_sql_engine,
    get_data
)
import base64
from io import BytesIO
import matplotlib.pyplot as plt

def init_app():
    # Create app
    app = Flask(
        __name__
        # template_foler = 'templates',
        # static_folder = 'static'
    )
    return app

app = init_app()
engine = create_sql_engine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    sql_query = 'SELECT year, count(*) as count FROM public.sk10189omdb_data group by year;'
    data = get_data(engine, sql_query)
    return render_template('visualize.html', data=data.values.tolist())

@app.route('/data_chart')
def data_chart():
    sql_query = 'SELECT year, count(*) as count FROM public.sk10189omdb_data group by year order by count DESC limit 10;'
    data = get_data(engine, sql_query)
    # print(data)
    ax = data.plot(kind='barh',
                   x='year',
                   y='count',
                   title='Time series plot of the number of movies released per year',
                   rot=60)
    buf = BytesIO()
    fig = plt.savefig(buf, format='png')

    data = base64.b64encode(buf.getvalue()).decode("ascii")
    
    return f"<img src='data:image/png;base64,{data}'/>"



if __name__ == '__main__':
    app.run(debug=True, port = 5000)

