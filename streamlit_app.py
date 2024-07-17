import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from movie_infos import read_movies_data, filter_movie_infos, poster_filter_func, sort_numeric_movie_infos, randomize_movie_infos, rating_filter_func, year_filter_func, title_filter_func, sort_string_movie_infos

#######################
# Page configuration
st.set_page_config(
    page_title="Movies Display",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded")


def sort_based_on_selection(movie_infos, sort_by, ascending):
    if ascending == "Ascending":
        ascending = True
    else:
        ascending = False
    if sort_by == "Rating":
        movie_infos = sort_numeric_movie_infos(movie_infos, 'rating', ascending=ascending)
    elif sort_by == "Year":
        movie_infos = sort_numeric_movie_infos(movie_infos, 'year', ascending=ascending)
    elif sort_by == "Title":
        movie_infos = sort_string_movie_infos(movie_infos, 'title', ascending=ascending)
    elif sort_by == "random":
        movie_infos = randomize_movie_infos(movie_infos)
    return movie_infos

def get_green_to_red(percent):
    # if 0 return grey
    if percent == 0:
        return "rgb(211,211,211)"
    percent *= 10
    percent = min(100, max(0, percent))
    r = 255 if percent < 50 else int(255 - (percent * 2 - 100) * 255 / 100)
    g = 255 if percent > 50 else int((percent * 2) * 255 / 100)
    b = 0
    return f"rgb({r},{g},{b})"
    
# Function to display a movie in the grid
def display_movie(movie_info):
    placeholder_image = "https://via.placeholder.com/150"
    placeholder_gif = "https://media.giphy.com/media/6Ud8LebVPM8uwIC9e1/giphy.gif?cid=790b76119hbx43vrxq3uhd8mjz7ouww8f43kh1xjn0j9bz7u&ep=v1_gifs_search&rid=giphy.gif&ct=g"
    
    # Check if the poster URL is valid
    poster_url = movie_info.get('poster', placeholder_image)
    
    try:
        response = requests.get(poster_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        st.image(image, use_column_width=True)
    except Exception:
        st.markdown(f"![Alt Text]({placeholder_gif})")

    st.markdown(f"**{movie_info['title']}**", help=movie_info['synopsis'])

    try: 
        rating = float(movie_info['rating'])
    except ValueError:
        rating = 0.0

    background_color = get_green_to_red(rating)

    if rating == 0.0:
        rating = "None"


    st.markdown(f"<span style='background-color: {background_color}; color: black; padding: 5px; border-radius: 5px;'>Rating: {rating}</span>",
                     unsafe_allow_html=True)
    
    st.markdown(f"Year: {movie_info['year']}")

def display_screen(movie_infos, num_movies_to_display):

    # If None found
    if num_movies_to_display == 0:
        st.write("No movies found with the given filters")
        st.markdown("![Alt Text](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnpmYnBsOHg5emp4b3lzaDMyYXZoZTFvc2ZoY3ptc25jd3J6OXExbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/o1wSLHms9t20ihdcEk/giphy.gif)")
        return

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
st.title("🎬FlixSync")

# Display the description
st.write(
    "Welcome to FlixSync! Here you can find filters to sync up the latest movies on Netflix available in BOTH countries. Inspired by the love for my girlfriend Joey and the distance between us, I wanted to make it easier for us to watch movies together by creating an effecient way to check which movies we both have."
)

# Read the movies data
movie_infos = read_movies_data()

# Filter out movies with no poster
movie_infos_all = filter_movie_infos(movie_infos, poster_filter_func)

num_movies = len(movie_infos_all)

#########################
# UI
#########################
st.sidebar.write("`Created by:`")
linkedin_url = "https://www.linkedin.com/in/carson-r-musser-/"
st.sidebar.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Carson Musser`</a>', unsafe_allow_html=True)


# Create a sidebar it will have a bunch of different components to determine filter
st.sidebar.title("🌎Country Sync Selection")

country1 = st.sidebar.radio("Select Country 1", ["United States", "Japan", "India"])
if country1 == "United States":
    country2 = st.sidebar.radio("Select Country 2", ["Japan", "India"])
elif country1 == "Japan":
    country2 = st.sidebar.radio("Select Country 2", ["United States", "India"])
elif country1 == "India":
    country2 = st.sidebar.radio("Select Country 2", ["United States", "Japan"])

st.sidebar.divider()
st.sidebar.title("🎛️Filters")

# add checkbox to include movies with no rating (0.0)
include_unrated = st.sidebar.checkbox("Include movies with no rating")
rating_filter = st.sidebar.slider("Min Max Rating", 0.0, 10.0, (0.0, 10.0))
year_filter = st.sidebar.slider("Release Years", 1900, 2024, (1900, 2024))
num_movies_to_display = st.sidebar.slider("Number of Movies to Display", min(num_movies,1), 1000, 100)

st.sidebar.divider()

st.sidebar.title("🔀Sort")
sort_by = st.sidebar.selectbox("Sort by", ["None", "Rating", "Year", "Title"])
# ascendring dsecending toggle
ascending = st.sidebar.radio("Ascending/Descending", ["Ascending", "Descending"])

# Add a search bar
search_query = st.text_input("🔍 Search movies", "")

# Add a search button
search_button = st.button("Search")

# Filter the movie_infos based on the search query
if search_query:
    movie_infos = filter_movie_infos(movie_infos, title_filter_func, search_query)
    movie_infos = filter_movie_infos(movie_infos, rating_filter_func, rating_filter[0], rating_filter[1], include_unrated)
    movie_infos = filter_movie_infos(movie_infos, year_filter_func, year_filter[0], year_filter[1])
    movie_infos = sort_based_on_selection(movie_infos, sort_by, ascending)
    num_movies = len(movie_infos)
    display_screen(movie_infos, min(num_movies, num_movies_to_display))
else:
    movie_infos = movie_infos_all
    movie_infos = filter_movie_infos(movie_infos, rating_filter_func, rating_filter[0], rating_filter[1], include_unrated)
    movie_infos = filter_movie_infos(movie_infos, year_filter_func, year_filter[0], year_filter[1])
    movie_infos = sort_based_on_selection(movie_infos, sort_by, ascending)
    num_movies = len(movie_infos)
    display_screen(movie_infos, min(num_movies, num_movies_to_display))





