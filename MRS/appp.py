import streamlit as st
import pickle
import pandas as pd
import requests  ##


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()

    # Check if 'poster_path' is present in the response
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        # Handle the case where 'poster_path' is not present
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters


# Load data
movies = pickle.load(open('/Users/tanishagarwal/Desktop/movie-recommender-systems/project mrs/MRS/venv/Resour/movies.pkl', 'rb'))
similarity = pickle.load(open('/Users/tanishagarwal/Desktop/movie-recommender-systems/project mrs/MRS/venv/Resour/similarity.pkl', 'rb'))
movies_list = movies["title"].values

st.header("Movie Recommender System") #

option = st.selectbox('Select the movie', movies_list)

if st.button('Recommend'):
    recom, posters = recommend(option)

    # Use st.columns instead of st.beta_columns
    # Use st.columns instead of st.beta_columns
    cols = st.columns(5)

    # Display recommended movies and posters in two rows with five columns each
    for i in range(15):
        with cols[i % 5]:
            st.text(recom[i])
            st.image(posters[i])




