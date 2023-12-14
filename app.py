# import required modules and database.
import base64
import json
from io import BytesIO
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import ast
from collections import Counter
import os

from db import *
from utils import *
from cosineSimilarity import *
from charts import *


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
    sql_query = "SELECT distinct(category) FROM public.ag8298_oscar_general"
    categories = get_data(engine, sql_query)
    categories = categories["category"].tolist()
    categories.sort()
    

    genre_chart = get_overall_genre_chart(get_genre_numbers())

    nomination_chart = get_overall_nomination_chart()


    return render_template('components/overall.html', 
                           range = range(2022, 1928, -1), 
                           categories = categories,
                           genres = genre_chart,
                           nomination = nomination_chart
                           )
    
#return diversity and social commentary scores for any movie
@app.route('/social-commentary-score', methods=['GET', 'POST'])
def social():
    cast_score = ''
    social_score = ''
    if request.method == 'POST':
        movie = request.form['movie']
        cast_score = return_cast_diversity_score(movie)
        social_score = return_movie_sentiment(movie)
        # Now you can store 'user_word' in your desired location
    return render_template('components/socialScore.html', message1=cast_score, message2=social_score)



#Oscar visualizations for a specific year
@app.route('/specific')
def specific():
    
    year = request.args.get('year')

    ratings_chart = get_ratings_chart(year)
    budget_chart = get_budget_chart(year)
    genres_chart = get_genres_chart(year)
    country_chart = get_country_chart(year)

    return render_template('components/specific.html', 
                        year = range(2019, 1928, -1),
                        #    film_info = film_info,
                        ratings = ratings_chart,
                        budget = budget_chart,
                        #    critics = critics_chart,
                        country = country_chart,
                        genres = genres_chart
                        )
    


#Search for a specific movie
@app.route('/search', methods=['GET', 'POST'])
def search():
    # integrate the tmdb api to get the movies from the search.
    args = request.args
    movies = None
    if "movie" in args.keys():
        movies = getMovie(request.args.get('movie'))["results"]
        #movies["genre_ids"] = getGenreFromId(movies["genre_ids"])
        for movie in movies:
            movie["genre_ids"] = (', ').join(getGenreFromId(movie["genre_ids"]))
    
    return render_template('components/search.html', movies= movies, search = args.get('movie') )


#Search feature for movie similarity.
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

#Advanced data analysis.
@app.route('/analysis')
def analysis():
    return render_template('components/analysis.html')
# This will be the route for visualizing predictions that we received from the model.
@app.route('/prediction')
def prediction():
    return render_template('components/prediction.html')

#project description
@app.route('/about')
def about():
    return render_template('components/about.html')


# API endpoints for getting the data from the database.
@app.route('/get-movie-list', methods = ['POST'])
def getMovielist():
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

        movie_info = getMovie(data['film'][0])['results'][0]

        print( 'film is     ' ,data )

        print( 'movie info is ', movie_info)

        final_data = {
            'data' : data.to_json(orient='records'),
            'img' : movie_info['poster_path']
        }

    
    return final_data
    

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

    return data.to_json(orient='records')


@app.route('/api/movie-similarity', methods = ['GET'])
def similarity_among_movies():
    movie1 = request.args.get('movie1')

    movie2 = request.args.get('movie2') 

    print('movies are', movie1, movie2)

    similar = getcosineSimilarity(movie1, movie2)

    return jsonify({'similarity': similar})


if __name__ == '__main__':
    app.run(debug=True, port = 5000)

