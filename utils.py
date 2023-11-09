import requests
import json

def getMovie( movie ):

    movies =  (requests
    .get(f"https://api.themoviedb.org/3/search/movie?query={movie}&api_key=398b5afb4273aa1b5552a5b91071c1e6")
    .json()
    )
    
    return movies
