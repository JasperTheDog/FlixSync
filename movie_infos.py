import json
import random

# Structure of movies_data.txt
# Each line is a json object, with a title, year, poster, synopsis, and rating, we will call this a movie_info

def read_movies_data(filename='movies_data.txt'):
    movie_infos = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            movie_info = json.loads(line.strip())
            movie_infos.append(movie_info)
    return movie_infos

# Create function that randomizes the order of the movies in file and saves to same file
def randomize_movies_data(filename='movies_data.txt'):
    movie_infos = read_movies_data(filename)
    random.shuffle(movie_infos)
    with open(filename, 'w', encoding='utf-8') as f:
        for movie_info in movie_infos:
            f.write(json.dumps(movie_info) + '\n')

# Sorting functions
def sort_numeric_movie_infos(movie_infos, property_name, ascending=True):
    sorted_movie_infos = sorted(movie_infos, key=lambda x: float(x[property_name]), reverse=not ascending)
    return sorted_movie_infos

def sort_string_movie_infos(movie_infos, property_name, ascending=True):
    sorted_movie_infos = sorted(movie_infos, key=lambda x: x[property_name], reverse=not ascending)
    return sorted_movie_infos

def randomize_movie_infos(movie_infos):
    random.shuffle(movie_infos)
    return movie_infos

# Filtering functions
def filter_movie_infos(movie_infos, filter_func, *args):
    filtered_movie_infos = filter(lambda x: filter_func(x, *args), movie_infos)
    return list(filtered_movie_infos)

def poster_filter_func(movie_info):
    poster = movie_info.get('poster')
    return poster and poster != "0" and poster != "N/A" and poster != ""

def rating_filter_func(movie_info, min_rating, max_rating, include_unrated=False):
    try:
        rating = float(movie_info.get('rating', 0.0))
    except (ValueError, TypeError):
        rating = 0.0
    
    if include_unrated and rating == 0.0:
        return True
    return min_rating <= rating <= max_rating

def year_filter_func(movie_info, min_year, max_year):
    try:
        year = int(movie_info.get('year'))
    except (ValueError, TypeError):
        year = 0
    return min_year <= year <= max_year

def title_filter_func(movie_info, title):
    return title.lower() in movie_info.get('title').lower()


