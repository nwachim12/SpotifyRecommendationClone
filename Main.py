# Main.py
import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
Client_ID = '0c755edd906444e384a385f2645a135e'
Client_Secret = '733cf80318b94d0e97c277547acd3a2f'

# Initialize Spotify API client
client_manager = SpotifyClientCredentials(client_id=Client_ID, client_secret=Client_Secret)
sp = spotipy.Spotify(client_credentials_manager=client_manager)

# Function to get album cover URL
def get_album_cover(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover = track["album"]["images"][0]["url"]
        return album_cover
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    dis = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    rec_names = []
    rec_posters = []
    for i in dis[1:6]:
        artist = music.iloc[i[0]].artist
        rec_posters.append(get_album_cover(music.iloc[i[0]].song, artist))
        rec_names.append(music.iloc[i[0]].song)
    return rec_names, rec_posters

# Streamlit application
st.header('Spotify Recommender System Clone')

# Load preprocessed data
try:
    with open('df.pkl', 'rb') as f:
        music = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()
except pickle.PickleError as e:
    st.error(f"Pickle error: {e}")
    st.stop()

# User interface
music_list = music['song'].values
selected_song = st.selectbox(
    "Select or type out a song from the dropdown",
    music_list
)

if st.button('Music Recommendation List'):
    rec_names, rec_posters = recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(rec_names[0])
        st.image(rec_posters[0])
    with col2:
        st.text(rec_names[1])
        st.image(rec_posters[1])
    with col3:
        st.text(rec_names[2])
        st.image(rec_posters[2])
    with col4:
        st.text(rec_names[3])
        st.image(rec_posters[3])
    with col5:
        st.text(rec_names[4])
        st.image(rec_posters[4])
