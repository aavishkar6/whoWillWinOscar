# import required modules and database.
import base64
import json
from io import BytesIO
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# import functions for reading and writing from the database
from db import (
    create_sql_engine,
    get_data
)

# import utility functions
from utils import (
    getMovie,
    getGenreFromId
)

#initialize flask app
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

#homepage route 
@app.route('/')
def index():
    return render_template('components/homepage.html')

#visualize route for the oscar's dataset
@app.route('/visualize')
def visualize():
    sql_query = 'SELECT year, count(*) as count FROM public.sk10189omdb_data group by year;'
    data = get_data(engine, sql_query)
    return render_template('components/visualize.html', data=data.values.tolist())

# This will be the route for visualizing predictions that we received from the model.
@app.route('/prediction')
def prediction():
    return render_template('components/prediction.html')

# Search route for searchin movies.
@app.route('/search', methods=['GET', 'POST'])
def search():
    # integrate the tmdb api to get the movies from the search.
    args = request.args
    movies = None
    if "movie" in args.keys():
        movies = getMovie(args.get('movie'))["results"]
        #movies["genre_ids"] = getGenreFromId(movies["genre_ids"])
        for movie in movies:
            movie["genre_ids"] = (', ').join(getGenreFromId(movie["genre_ids"]))
    
    return render_template('components/search.html', movies= movies, search = args.get('movie') )

@app.route('/about')
def about():
    return render_template('components/about.html')


if __name__ == '__main__':
    app.run(debug=True, port = 5000)

