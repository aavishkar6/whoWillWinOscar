import requests
import json
import os
import Levenshtein
from fuzzywuzzy import process



# from dotenv import load_dotenv

# load_dotenv()

def getMovie( movie ):
    apiKey = os.getenv("TMDB_API")
    movies =  (requests
    .get(f"https://api.themoviedb.org/3/search/movie?query={movie}&api_key={apiKey}")
    .json()
    )
    print(movies)
    
    return movies

def getGenreFromId( genre_ids ):
    res = []
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzOThiNWFmYjQyNzNhYTFiNTU1MmE1YjkxMDcxYzFlNiIsInN1YiI6IjYzZjY2OGUwNjljNzBmMDA4MjIxN2FlMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.R2oKaK7HGt_aDFwA48zNJFIlGu61lU_eV6HHJgBhJw8"
    }

    response = requests.get(url, headers=headers).json()
    
    for genre in response["genres"]:
        if genre["id"] in genre_ids:
            res.append(genre["name"])

    return res

def getSimilarMovies( movie ):
    with open('file.txt', 'r') as f:
        data = f.read()

    data = data.split('\n')

    # movieList =  [w for w in data if Levenshtein.distance(movie, w) <= 2]
    movieList = process.extractBests(movie, data, score_cutoff=50)

    return movieList

def getAddData( imdb_id ):

    url = f"https://api.themoviedb.org/3/find/tt{imdb_id}?external_source=imdb_id"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzOThiNWFmYjQyNzNhYTFiNTU1MmE1YjkxMDcxYzFlNiIsInN1YiI6IjYzZjY2OGUwNjljNzBmMDA4MjIxN2FlMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.R2oKaK7HGt_aDFwA48zNJFIlGu61lU_eV6HHJgBhJw8"
    }

    response = requests.get(url, headers=headers).json()


    return response

def getCastData ( id ) :
    
    url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzOThiNWFmYjQyNzNhYTFiNTU1MmE1YjkxMDcxYzFlNiIsInN1YiI6IjYzZjY2OGUwNjljNzBmMDA4MjIxN2FlMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.R2oKaK7HGt_aDFwA48zNJFIlGu61lU_eV6HHJgBhJw8"
    }
    
    response = requests.get(url, headers=headers).json()

    actors = []
    for cast in response['cast']:
        actors.append(cast['name'])

    return actors[:5]
