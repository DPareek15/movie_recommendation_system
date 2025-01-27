import gzip
import urllib

import dill
import requests
import streamlit as st

api_key = st.secrets["OMDB_API_KEY"]

movies = dill.load(open("data/movies_data.pkl", "rb"))
with gzip.open("data/similarity.pkl.gz", "rb") as f:
    similarity_matrix = dill.load(f)


def recommend_movies(movie, num=5):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity_matrix[movie_index]
    id_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1 : num + 1
    ]
    rec_list = []

    for item in id_list:
        rec_list.append({"movie_id": item[0], "title": movies.iloc[item[0]].title})

    return rec_list


def get_details(movie_list):
    movies_data = []
    with st.spinner("Fetching movies..."):
        for item in movie_list:
            name = urllib.parse.quote_plus(item["title"])
            url = f"http://www.omdbapi.com/?apikey={api_key}&t={name}"
            res = requests.get(url)
            data = res.json()
            movie_data = []
            if data["Response"] == "True":
                data_dict = {
                    "Title": data["Title"],
                    "Genre": data["Genre"],
                    "Year released": data["Year"],
                    "Director": data["Director"],
                    "Actors": data["Actors"],
                    "Runtime": data["Runtime"],
                    "Plot": data["Plot"],
                }
                movie_data.append(data_dict)
                movie_data.append(data["Poster"])
            else:
                movie_i = movies[movies["title"] == item["title"]].index[0]
                movie_dict = movies.iloc[movie_i].to_dict()
                data_dict = {
                    "Title": movie_dict["title"],
                    "Genre": movie_dict["genres"],
                    "Year released": movie_dict["release_date"],
                    "Director": movie_dict["crew"],
                    "Actors": movie_dict["cast"],
                    "Runtime": movie_dict["runtime"],
                    "Plot": movie_dict["overview"],
                }
                movie_data.append(data_dict)
            movies_data.append(movie_data)

    return movies_data


st.title("Movie Recommender System")
st.divider()
selected_movie = st.selectbox("Select the movie:", movies["title"].values)
movie_num = st.slider(
    "Number of movies to recommend:", min_value=1, max_value=10, step=1, value=5
)

movie_dict = {}

if st.button(
    "Recommend", type="primary", help="Click this button to get recommendations"
):
    rec_dict = recommend_movies(selected_movie, movie_num)
    movie_dict = get_details(rec_dict)
    m_list = {"hello"}

st.divider()

for item in movie_dict:
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            if len(item) == 2:
                st.image(item[1])
        with col2:
            for key, value in item[0].items():
                st.write(f"{key}: {value}")

if movie_dict != {}:
    st.divider()
