import json

# Structure of movies_data.txt
# Each line is a json object, with a title, year, poster, synopsis, and rating, we will call this a movie_info

def read_movies_data(filename='movies_data.txt'):
    movie_infos = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            movie_info = json.loads(line.strip())
            movie_infos.append(movie_info)
    return movie_infos


def sort_movie_infos(movie_infos, property_name):
    sorted_movie_infos = sorted(movie_infos, key=lambda x: x[property_name])
    return sorted_movie_infos


