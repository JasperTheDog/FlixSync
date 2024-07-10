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

def sort_numeric_movie_infos(movie_infos, property_name, ascending=True):
    sorted_movie_infos = sorted(movie_infos, key=lambda x: float(x[property_name]), reverse=not ascending)
    return sorted_movie_infos

def sort_string_movie_infos(movie_infos, property_name, ascending=True):
    sorted_movie_infos = sorted(movie_infos, key=lambda x: x[property_name], reverse=not ascending)
    return sorted_movie_infos

def filter_movie_infos(movie_infos, filter_func):
    filtered_movie_infos = filter(filter_func, movie_infos)
    return list(filtered_movie_infos)

def poster_filter_func(movie_info):
    poster = movie_info.get('poster')
    return poster and poster != "0" and poster != "N/A" and poster != ""

def randomize_movie_infos(movie_infos):
    random.shuffle(movie_infos)
    return movie_infos

