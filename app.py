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
    getGenreFromId,
    getSimilarMovies
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

#visualize route for the oscar's overall dataset.
@app.route('/overall')
def visualize():
    sql_query = "SELECT distinct(category) FROM public.ag8298_oscar_general" ;
    categories = get_data(engine, sql_query)
    categories = categories["category"].tolist()
    return render_template('components/overall.html', range = range(1927, 2021), categories = categories)


# this will be the route for visualizing specific year movie.
@app.route('/specific')
def specific():
    
    return "<h1>SPECIFIC</h1>"

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

# Search feature for movie similarity.
@app.route('/similarity', methods=['GET', 'POST'])
def similarity():
    """
        1. get the movies from the user.
        2. get the movies info from the api or database.
        3. feed it to the movie similarity function.
        4. get the similar movies.
        5. return the similar movies to the user.
    """

    return render_template('components/similarity.html')


@app.route('/about')
def about():
    return render_template('components/about.html')














# API endpoints for getting the data from the database.

@app.route('/get-movie-list', methods = ['POST'])
def getMovie():
    movie = request.get_json()

    movieList = getSimilarMovies(movie.get('selectedMovie'))


    

    return jsonify(movieList)

    
        

    

@app.route('/api/nominee', methods = ['GET'])
def nominee():

    category = request.args.get('category')   
    print(category)

    sql_query = f"SELECT year_awarded as year, count(distinct(film)) as count FROM public.ag8298_oscar_general where category=\"{category}\" group by year_awarded;"
    data = get_data(engine, sql_query)
    print(data)
    print(type(data))
    return data.to_json(orient='records')


@app.route('/api/winner', methods = ['GET'])
def winner():
    
    year = request.args.get('year')
    category = request.args.get('category')

    print(category)
    print(year)
    if (year and category):
        sql_query = f"SELECT * FROM public.ag8298_oscar_general where year_awarded = \"{year}\" and winner =\"True\" and category=\"{category}\";"
        data = get_data(engine, sql_query)
        # print(data)
        return data.to_json(orient='records')
    

@app.route('/api/best_rated_oscar_movies', methods = ['GET'])
def best_rated_oscar_movies():

    category  = request.args.get('category')

    print('category is ', category)
    if ( not category):
        sql_query = "SELECT film, rate FROM public.ag8298_oscar_detailed where position=\"Winner\" order by rate desc limit 15;"
        data = get_data(engine, sql_query)
    else :
        sql_query = f"SELECT film, rate FROM public.ag8298_oscar_detailed where position=\"{category}\" order by rate desc limit 15;"
        data = get_data(engine, sql_query)

    print(data)
    return data.to_json(orient='records')


@app.route('/api/highest_budget_movie', methods = ['GET'])
def highest_budget_movie():
    category  = request.args.get('category')

    print('category is ', category)
    if ( not category):
        sql_query = "SELECT film, budget FROM public.ag8298_oscar_detailed where position = \"Winner\" order by budget desc limit 20;"
        data = get_data(engine, sql_query)
    else :
        sql_query = f"SELECT film, budget FROM public.ag8298_oscar_detailed where position = \"{category}\" order by budget desc limit 20;"
        data = get_data(engine, sql_query)

    data = get_data(engine, sql_query)
    print(data)
    return data.to_json(orient='records')







if __name__ == '__main__':
    app.run(debug=True, port = 5000)

