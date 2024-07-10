import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

def replace_html_entities(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        file_data = file.read()

    # Replace &#39; with '
    file_data = file_data.replace('&#39;', "'")

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(file_data)

def fetch_movies_in_countries_jp_us(filename, offset=0):

    url = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"

    querystring = {"country_list": "267,78", "order_by": "rating", "type": "movie", "country_andorunique": "and",
                   "offset": offset}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "unogs-unogs-v1.p.rapidapi.com"
    }

    print(RAPIDAPI_KEY)

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        total_movies = data.get('Object', {}).get('total', 0)
        movies_data = data.get('results', [])

        # Determine file mode based on offset
        mode = 'a' if offset > 0 else 'w'

        with open(filename, mode, encoding='utf-8') as f:
            for movie in movies_data:
                movie_info = {
                    "title": movie.get('title'),
                    "rating": movie.get('rating'),
                    "synopsis": movie.get('synopsis'),
                    "year": movie.get('year'),
                    "poster": movie.get('poster')
                }
                # Convert dictionary to JSON string and write to file
                json.dump(movie_info, f, ensure_ascii=False)
                f.write('\n')

        print(f"Received {len(movies_data) + offset} movies out of {total_movies}")

        return total_movies, offset + len(movies_data)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return 0, offset


if __name__ == '__main__':
    offset = 0
    num_requests = 1
    filename = 'test.txt'

    # Clean up existing movies_data.txt if offset is 0
    if offset == 0 and os.path.exists(filename):
        os.remove(filename)

    for _ in range(num_requests):
        total_movies, offset = fetch_movies_in_countries_jp_us(filename, offset)
        if offset >= total_movies:
            print("All movies fetched.")
            break

    print(f"Total movies fetched: {offset}")
    replace_html_entities(filename)