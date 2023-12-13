
import ast
from collections import Counter

from db import (
    create_sql_engine,
    get_data
)



engine = create_sql_engine()

def get_country_chart(year):
    sql_query = f"SELECT film, year, position, duration, genres,country FROM public.ag8298_oscar_detailed where year = '{year}';"
    data = get_data(engine, sql_query)

    d = data['country'].tolist()

    country = [country.strip() for sublist in d for country in ast.literal_eval(sublist)]

    country_counts = Counter(country)

    chart_data = {
        "type": "bar",
        "data": {
            "labels": [genre for genre in country_counts.keys()],
            "datasets": [{
                "label": 'Countries the movie was produced in.',
                "data": [num for num in country_counts.values()],
                "backgroundColor": [
                    'rgba(255,99,132,1)', 
                    'rgba(54, 162, 235, 1)', 
                    'rgba(255, 206, 86, 1)', 
                    'rgba(75, 192, 192, 1)', 
                    'rgba(153, 102, 255, 1)', 
                    'rgba(255, 159, 64, 1)'
                    ],
                "borderColor": [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                "borderWidth": 1
            }]
        },
        "options": {
            "responsive"  : 'True',
            "indexAxis": 'y',
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True
                    }
                }]
            }
        }
    }

    return chart_data

def get_genres_chart(year):
    sql_query = f"SELECT film, year, position, duration, genres,country FROM public.ag8298_oscar_detailed where year = '{year}';"
    data = get_data(engine, sql_query)

    
    genres_count = data['genres'].tolist()

    # Parse the strings into actual lists and flatten the list
    genres = [genre.strip() for sublist in genres_count for genre in ast.literal_eval(sublist)]

    # Count the occurrences of each genre
    genre_counts = Counter(genres)

    chart_data = {
        "type": "bar",
        "data": {
            "labels": [genre for genre in genre_counts.keys()],
            "datasets": [{
                "label": 'Genres of the movies',
                "data": [num for num in genre_counts.values()],
                "backgroundColor": [
                    'rgba(255,99,132,1)', 
                    'rgba(54, 162, 235, 1)', 
                    'rgba(255, 206, 86, 1)', 
                    'rgba(75, 192, 192, 1)', 
                    'rgba(153, 102, 255, 1)', 
                    'rgba(255, 159, 64, 1)'
                    ],
                "borderColor": [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                "borderWidth": 1
            }]
        },
        "options": {
            "responsive"  : 'True',
            "indexAxis": 'y',
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True
                    }
                }]
            }
        }
    }

    return chart_data   

def get_budget_chart(year):
    sql_query = f"SELECT film, budget, position FROM public.ag8298_oscar_detailed where year = '{year}' order by budget desc;"
    data  = get_data(engine, sql_query)

    colors = ['yellow' if data['position'][i] == 'Winner' else 'red' for i in range(len(data['position']))]


    chart_data = {
        "type": "bar",
        "data": {
            "labels": data["film"].tolist(),
            "datasets": [{
                "label": 'Budget of the movies',
                "data": data["budget"].tolist(),
                "backgroundColor": colors,
                "borderColor": [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                "borderWidth": 1
            }]
        },
        "options": {
            "responsive"  : 'True',
            "indexAxis": 'y',
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True
                    }
                }]
            }
        }
    }

    return chart_data

def get_ratings_chart(year):
    sql_query = f"SELECT film, rate, position FROM public.ag8298_oscar_detailed where year = '{year}' order by rate desc;"
    data = get_data(engine, sql_query)

    colors = ['rgba(255, 206, 86, 1)' if data['position'][i] == 'Winner' else 'rgba(255,99,132,1)' for i in range(len(data['position']))]

    print(data)

    chart_data = {
        "type": "bar",
        "data": {
            "labels": data["film"].tolist(),
            "datasets": [{
                "label": 'Ratings of the movies',
                "data": data["rate"].tolist(),
                "backgroundColor": colors,
                "borderColor": [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                "borderWidth": 1
            }]
        },
        "options": {
            "responsive"  : 'True',
            "indexAxis": 'y',
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True
                    }
                }]
            }
        }
    }

    return chart_data


def get_overall_genre_chart(genre_dict):

    chart_data = {
    "type": "bar",
    "data": {
        "labels": [genre for genre in genre_dict.keys()],
        "datasets": [{
            "data": [num for num in genre_dict.values()],
            "backgroundColor": [
                'rgba(255,99,132,1)', 
                'rgba(54, 162, 235, 1)', 
                'rgba(255, 206, 86, 1)', 
                'rgba(75, 192, 192, 1)', 
                'rgba(153, 102, 255, 1)', 
                'rgba(255, 159, 64, 1)'
            ],
            "borderColor": [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            "borderWidth": 1
        }]
    },
    "options": {
    "plugins": {
            "title": {
                "display": True,
                "text": 'Genre of the Oscar nominee movies from 1928 to 2019.',
                "font": {
                    "size": 30
                },
                "color": 'rgba(181, 186, 37, 0.673)',
                "padding": 20,
                "position": 'top'
            }
            },
            "responsive": True,
            "indexAxis": 'y',
            "scales": {
                "y": {
                    "ticks": {
                        "beginAtZero": True
                    }
                }
            }
        }
    }


    return chart_data

def get_overall_nomination_chart() :
    sql_query_1 = f"SELECT film,year,rate from public.ag8298_oscar_detailed where position = 'Winner' order by year desc;"
    winner_data = get_data(engine, sql_query_1)

    sql_query_2 = f"""SELECT main.film, main.year, main.rate
                        FROM public.ag8298_oscar_detailed main 
                        JOIN 
                            (SELECT year, MAX(rate) as max_rate 
                            FROM public.ag8298_oscar_detailed 
                            WHERE position = 'Nominee' 
                            GROUP BY year) sub 
                        ON main.year = sub.year AND main.rate = sub.max_rate 
                        WHERE main.position = 'Nominee' 
                        ORDER BY main.year DESC;
                    """
    nominee_data = get_data(engine, sql_query_2)


    chart_data =  {
            'type': 'line',
            'data': {
                'labels': [year for year in range(2019, 1928, -1)],
                'datasets': [
                    {
                        'label': 'Winner Ratings',
                        'data': winner_data['rate'].tolist(),
                        'fill': 'false',
                        'borderColor': 'rgb(75, 192, 192)',
                        'tension': '0.1',
                    },
                    {
                        'label': 'Nominee Ratings',
                        'data': nominee_data['rate'].tolist(),
                        'fill': 'false',
                        'borderColor': 'rgb(255, 99, 132)',
                        'tension': '0.1',
                    }
                ]
            },
            'options': {
                'scales': {
                    'y': {
                        'beginAtZero': 'true',
                        'max' : '10',
                        'min' : '5'
                    }
                }
            }
        }
    
    return chart_data

def get_genre_numbers():
    sql_query = f"SELECT genres from public.ag8298_oscar_detailed;"

    data = get_data(engine, sql_query)

    genre_count = data['genres'].tolist()

    # Parse the strings into actual lists and flatten the list
    genres = [genre.strip() for sublist in genre_count for genre in ast.literal_eval(sublist)]

    # Count the occurrences of each genre
    genre_counts = Counter(genres)


    return genre_counts
