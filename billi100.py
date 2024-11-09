import os
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")



user = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user}/" ,headers= header)
soup  = BeautifulSoup(response.text , "html.parser")

songs_titles = soup.select("li h3.c-title")

songs_list = []
for song in songs_titles :
    title =song.get_text(strip=True)
    if title:
        songs_list.append(title)

# authentication and request

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        client_id= SPOTIPY_CLIENT_ID,
        client_secret = SPOTIPY_CLIENT_SECRET,
        redirect_uri= SPOTIPY_REDIRECT_URI ,
        scope= "playlist-modify-private playlist-modify-public"
    )
)

track_uris = []

# pprint(sp.search(q=songs_list[1], type="track", limit=1))
for song in songs_list:
    
    try:
        # spotify search for the song
        results = sp.search(q=song, type="track", limit=1)
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            track_uris.append(track_uri)
            print(f"found URI for '{song}':{track_uri}")
        else:
            print(f"UrI is not found for '{song}'")
    except Exception as ex:
        print(f"Error searching for '{song}': {ex}")

user_id = sp.current_user()["id"]
playlist_name = f"Top-songs-{user}"

new_playlist = sp.user_playlist_create(
    user=user_id,
    name=playlist_name,
    public=False,  # Set to True if you want it to be public
    description="Playlist created using Python and Spotipy"
)

playlist_id = new_playlist["id"]
print(f"Playlist '{playlist_name}' created successfully with ID: {playlist_id}")


if track_uris:
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
    print("Tracks added to the playlist successfully!")
else:
    print("No tracks were added because no URIs were found.")








