import pickle
import pandas as pd
import numpy as np
import streamlit as st
import requests
import json



file1 = open("./data/movie_data.pkl","rb")
file2 = open("./data/similarity_matrix.pkl","rb")

movies = pickle.load(file1)
similarity_of_movies = pickle.load(file2)


def recommender(movie):
    result = []
    count = 0
    sim = similarity_of_movies[movies[movies["title"]==movie].index[0]]
    sorted_sim = sorted(enumerate(sim), reverse=True, key = lambda x: x[1])
    for index, val in sorted_sim:
        result.append(movies.title[index])
        count+=1
        if count>8:
            break
    return result[1:]

def get_poster(movie_list):
    poster_paths = []
    movie_info = []
    for i in movie_list:
        movie_path = 'https://api.themoviedb.org/3/search/movie?query={}&api_key=7b76feafee6c77ba0d8ca4958e815ac5'.format(i)
        data = requests.get(movie_path)
        data = data.json()
        poster_paths.append("https://image.tmdb.org/t/p/original/"+ data["results"][0]["poster_path"])
        movie_info.append("https://www.themoviedb.org/movie/"+str(data["results"][0]["id"]))
    
    return poster_paths, movie_info


## Streamlit Code:
def run_app():
    st.title("Netflix Movie Recommender")
    selected_movie = st.selectbox(
        "Select the movie you are watching!",
        movies["title"].values
        )

    if st.button("Recommend Movies"):
        names = recommender(selected_movie)
        images, urls = get_poster(names)

        st.subheader("Recommended for you...")

        col0,col1,col2,col3 = st.columns(4, gap= "medium")
        col,col5,col6,col7 = st.columns(4, gap= "medium")
        cols = [col0,col1,col2,col3,col,col5,col6,col7]

        for i in range(0,8):
            with cols[i]:
                st.image(images[i])
                st.text(names[i])
                link_to_info = urls[i]
                st.markdown("""
                    <a href={}><button style="background-color:Black; color: White">More Info</button></a>
                """.format(link_to_info),
                unsafe_allow_html= True
                )


if __name__ == "__main__":
    run_app()
