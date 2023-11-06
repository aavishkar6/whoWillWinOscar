from flask import Flask, render_template, request, redirect, url_for, flash
from db import (
    create_engine,
    get_data
)

def init_app():
    # Create app
    app = Flask(
        __name__
        # template_foler = 'templates',
        # static_folder = 'static'
    )
    return app

app = init_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/data_chart')
def data_chart():
    return render_template('data_chart.html')



if __name__ == '__main__':
    app.run(debug=True, port = 5000)

