import requests
import json

def getMovie( movie ):

    movies =  (requests
    .get(f"https://api.themoviedb.org/3/search/movie?query={movie}&api_key=398b5afb4273aa1b5552a5b91071c1e6")
    .json()
    )
    
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
