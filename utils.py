import requests
import json
import os
import Levenshtein
from fuzzywuzzy import process
from openai import OpenAI


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

def get_completion(prompt, model="gpt-3.5-turbo"):
    # OPENAI_API_KEY = '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'
    OPENAI_API_KEY = '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'
    client = OpenAI(api_key=OPENAI_API_KEY)

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


def analyze_movie(name, description):
  prompt = f"""
    The following text provided is the name of a movie. Using your prior knowledge of the movie, give it a score between 1 - 10 that expresses how much the movie revolves around social commentary. For example, Parasite would rank around a 9 or 10, as it explores themes of class and wealth disparities. If you don't have prior knowlege of the movie, then use the description to hypothesize your answer. Output your response in the format '[movie name]'s social commentary score is [score] because [explanation].', where the model fills in the brackets.
    Review text: {name, description}
    """
  return get_completion(prompt)

def return_cast_diversity_score(movie_name):
  data = get_movie_data(movie_name)
  cast = data['top_cast_names']
  directors = data['directors']
  return analyze_cast(movie_name, cast, directors)

def analyze_cast(name, cast, directors):
  prompt = f"""
    The following text provided is the name of a movie, the top cast members, and the directors. Using your knowledge of these people, give it a score between 1 - 100 that expresses the rough percentage of the diversity of the cast. For example, if the half of the cast belongs to a minority group (woman or racial minority), then the diversity score would be 50). Even if it is a rough, inaccurate estimate, that's fine, we're promoting more diversity in hollywood. just give us a number please. provide a number and only a number.
    Review text: {name, cast, directors}
    """
  return get_completion(prompt)

def return_movie_sentiment(movie_name):
  data = get_movie_data(movie_name)
  description = data['description']
  return analyze_movie(movie_name, description)


def get_movie_data(movie_name):
  # api_key = '390b5cfbeebb1ba623c4041babe57de9'
  api_key = '398b5afb4273aa1b5552a5b91071c1e6'
  # api_key = 
  search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}'
  response = requests.get(search_url)
  data = response.json()
  print(data)
  movie_id = data['results'][0]['id']

  details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits'
  response = requests.get(details_url)
  movie_details = response.json()
  #return movie_details

  movie_data = {}

  if movie_details['budget']:
    movie_data['budget'] = movie_details['budget']

  if movie_details['overview']:
    movie_data['description'] = movie_details['overview']

  if movie_details['genres']:
    genres = []
    for genre in movie_details['genres']:
      genres.append(genre['name'])
    movie_data['genres'] = genres

  if movie_details['original_language']:
    movie_data['original_language'] = movie_details['original_language']

  if movie_details['original_title']:
    movie_data['original_title'] = movie_details['original_title']

  if movie_details['popularity']:
    movie_data['popularity'] = movie_details['popularity']

  if movie_details['production_companies']:
    production_companies = []
    for company in movie_details['production_companies']:
      production_companies.append(company['name'])
    movie_data['production_companies'] = production_companies

  if movie_details['production_countries']:
    production_countries = []
    for country in movie_details['production_countries']:
      production_countries.append(country['name'])
    movie_data['production_countries'] = production_countries

  if movie_details['release_date']:
    movie_data['release_date'] = movie_details['release_date']

  if movie_details['revenue']:
    movie_data['revenue'] = movie_details['revenue']

  if movie_details['runtime']:
    movie_data['runtime'] = movie_details['runtime']

  if movie_details['tagline']:
    movie_data['tagline'] = movie_details['tagline']

  if movie_details['vote_average']:
    movie_data['vote_average'] = movie_details['vote_average']

  if 'credits' in movie_details and 'cast' in movie_details['credits']:
        cast_list = movie_details['credits']['cast']
        top_cast_names = [cast_member['name'] for cast_member in cast_list[:10]]  # Get the top 10 cast members
        movie_data['top_cast_names'] = top_cast_names
  if 'credits' in movie_details and 'crew' in movie_details['credits']:
    crew_list = movie_details['credits']['crew']
    movie_data['directors'] = [crew_member['name'] for crew_member in crew_list[:2] if 'Directing' in crew_member['department']]

  return movie_data
