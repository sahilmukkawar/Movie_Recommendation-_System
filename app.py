import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url, timeout=10)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path', '')
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # Update with the correct column name
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))  # Fetch poster from API

    return recommended_movies, recommended_movie_posters


# Load the pickled files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

# Selectbox for movie titles
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations",
    movies['title'].values
)

# Recommend button
if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Display the recommended movies and their posters
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])