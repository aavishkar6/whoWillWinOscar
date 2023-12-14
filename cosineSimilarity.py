import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
# nltk.download('punkt')

from utils import (
    getAddData,
    getGenreFromId,
    getCastData
)
def getcosineSimilarity(movie1, movie2 ):

    with open('imdbId.json', 'r') as f:
        data = json.load(f)


    mov1id = data[movie1]
    mov2id = data[movie2]

    # first two letter of the movie id is tt, so we need to remove it
    print( mov1id[2:], mov2id[2:])

    movie1 = processtext(getMovieDetails(mov1id[2:]))

    movie2 = processtext(getMovieDetails(mov2id[2:]))

    similarity = cosineSimilarity( movie1, movie2 )

    print('similarity is', similarity)

    return similarity

def cosineSimilarity(text1, text2):
    """
        Takes in two texts and returns the cosine similarity score between the two texts
    """
    # Vectorizing the texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculating cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_sim[0][0]


def getMovieDetails( imdb_id ):
    """
        Takes in imdb_id and returns a dictionary with keys as features described above and values as values
    """
    movie = {}
    results = getAddData( imdb_id )['movie_results'][0]
    movie['title'] = results['title']
    movie['genres'] = (' ').join(getGenreFromId(results['genre_ids']))
    movie['cast'] = (' ').join(getCastData( results['id'] ))
    movie['overview'] = results['overview']

    return movie


def processtext( movie ) :
    str = ''
    for keys in movie:
        print( f"{keys} : {movie[keys]}")
        str += movie[keys] + ' , '

    return text_preprocessing(str)

def text_preprocessing(str):
    
    stop_words = stopwords.words('english')

    str = str.lower().strip()

    words = str.replace('http\S+|www.\S+|@|%|:|,|', '')

    words = word_tokenize(words)
    
    filtered_text = [word for word in words if word.lower() not in stop_words]
    
    return ' '.join(filtered_text)

    return words
    
