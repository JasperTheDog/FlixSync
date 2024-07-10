import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from movie_infos import read_movies_data, filter_movie_infos, poster_filter_func, sort_numeric_movie_infos, randomize_movie_infos

#######################
# Page configuration
st.set_page_config(
    page_title="Movies Display",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded")

def get_green_to_red(percent):
    percent *= 10
    percent = min(100, max(0, percent))
    r = 255 if percent < 50 else int(255 - (percent * 2 - 100) * 255 / 100)
    g = 255 if percent > 50 else int((percent * 2) * 255 / 100)
    b = 0
    return f"rgb({r},{g},{b})"
    
# Function to display a movie in the grid
def display_movie(movie_info):
    placeholder_image = "https://via.placeholder.com/150"
    
    # Check if the poster URL is valid
    poster_url = movie_info.get('poster', placeholder_image)
    
    try:
        response = requests.get(poster_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        st.image(image, use_column_width=True)
    except Exception:
        st.image(placeholder_image, use_column_width=True)

    st.markdown(f"**{movie_info['title']}**")

    rating = float(movie_info['rating'])

    background_color = get_green_to_red(rating)

    # Style the rating display
    st.markdown(f"<span style='background-color: {background_color}; color: black; padding: 5px; border-radius: 5px;'>Rating: {rating}</span>",
                 unsafe_allow_html=True)
    
    st.markdown(f"Year: {movie_info['year']}")

def display_screen(movie_infos, num_movies_to_display):

    # Create a grid layout to display the movies
    num_columns = 5
    num_rows = num_movies_to_display // num_columns + (1 if num_movies_to_display % num_columns != 0 else 0)

    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            idx = i * num_columns + j
            if idx < num_movies_to_display:
                with cols[j]:
                    display_movie(movie_infos[idx])



# Display the title
st.title("FlixSync")

# Display the description
st.write(
    "Welcome to FlixSync! Here you can find filters to sync up the latest movies on Netflix available in BOTH countries. Inspired by the love for my girlfriend Joey and the distance between us, I wanted to make it easier for us to watch movies together."
)

# Read the movies data
movie_infos = read_movies_data()

# Filter out movies with no poster
movie_infos = filter_movie_infos(movie_infos, poster_filter_func)

# Sort the movies by rating
movie_infos_all = sort_numeric_movie_infos(movie_infos, 'rating', False)

movie_infos_all = randomize_movie_infos(movie_infos_all)

# Add a search bar
search_query = st.text_input("Search movies", "")

# Add a search button
search_button = st.button("Search")

# Filter the movie_infos based on the search query
if search_button:
    if search_query:
        movie_infos = filter_movie_infos(movie_infos_all, lambda movie: search_query.lower() in movie['title'].lower())
        print(search_query.lower())
    else:
        movie_infos = movie_infos_all
    
    # Display the filtered movies in a grid format
    num_movies_to_display = min(55, len(movie_infos))
    display_screen(movie_infos, num_movies_to_display)





