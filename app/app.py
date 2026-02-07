import pickle 
import streamlit as st
import pandas as pd
import requests 
from concurrent.futures import ThreadPoolExecutor, as_completed

@st.cache_data
def load_data():
    """Cache pickle files to avoid reloading on every rerun"""
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

@st.cache_data
def fetch_movie_details(movie_id):
    """Cache poster URLs and IMDB IDs to avoid repeated API calls"""
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url, timeout=5)
        
        if data.status_code != 200:
            return None, None
        
        data = data.json()
        
        # Check for API errors
        if 'status_code' in data and data['status_code'] != 1:
            return None, None
        
        poster_path = data.get('poster_path')
        imdb_id = data.get('imdb_id')
        
        poster_url = None
        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
        
        imdb_url = None
        if imdb_id:
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
        
        return poster_url, imdb_url
    except Exception as e:
        return None, None

def fetch_movie_details_parallel(movie_ids):
    """Fetch multiple movie details (posters and IMDB links) in parallel for faster loading"""
    details = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_movie_details, mid): mid for mid in movie_ids}
        for future in as_completed(futures):
            movie_id = futures[future]
            try:
                details[movie_id] = future.result()
            except:
                details[movie_id] = (None, None)
    return details

def recommend(movie, movies, similarity):
     movie_index = movies[movies['title'] == movie].index[0]
     movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x:x[1])[1:6]

     recommended_movies = []
     movie_ids = []
     for i in movies_list:
         movie_id = movies.iloc[i[0]].id
         movie_ids.append(movie_id)
         recommended_movies.append(movies.iloc[i[0]].title)
     
     # Fetch all posters and IMDB links in parallel
     details_dict = fetch_movie_details_parallel(movie_ids)
     recommended_movie_posters = [details_dict[mid][0] for mid in movie_ids]
     recommended_movie_imdb_urls = [details_dict[mid][1] for mid in movie_ids]
     
     return recommended_movies, recommended_movie_posters, recommended_movie_imdb_urls

movies, similarity = load_data()


st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie_name = st.selectbox( "choose a movie" , movies['title'].values )

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_imdb_urls = recommend(selected_movie_name, movies, similarity)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    
    for idx, col in enumerate(columns):
        with col:
            movie_name = recommended_movie_names[idx]
            movie_poster = recommended_movie_posters[idx]
            movie_imdb = recommended_movie_imdb_urls[idx]
            
            # Display movie title as link if available
            if movie_imdb:
                st.markdown(f"[{movie_name}]({movie_imdb})")
            else:
                st.text(movie_name)
            
            # Display poster if available
            if movie_poster:
                st.image(movie_poster)
            else:
                st.info("Poster not available")


