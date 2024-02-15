import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random


# Replace these with your own credentials. You will need it to have the playlist created in your account
client_id = ""
client_secret = ""

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = 'https://anandpagnis.github.io/PROJECTS/index.html' 
#preferably your own URI but it works regardless, just put in https://google.com/ in case mine doesnt work.

# Create a Spotify authentication object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='playlist-modify-public'))

def search_playlists_by_name(name, limit=1):
    results = sp.search(q=name, type='playlist', limit=limit)

    playlists = []
    for playlist in results['playlists']['items']:
        playlists.append({
            'name': playlist['name'],
            'owner': playlist['owner']['display_name'],
            'id': playlist['id']
        })

    return playlists

def get_random_songs_from_playlist(playlist_id, num_songs):
    playlist_tracks = sp.playlist_tracks(playlist_id, limit=num_songs)['items']

    random.shuffle(playlist_tracks)
    num = random.randint(1, 5)
    selected_songs = playlist_tracks[num:num+num_songs]

    songs = []
    for song in selected_songs:
        track = song['track']
        songs.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        })

    return songs

def get_random_playlists(name, limit=10):
    playlist_results = []
    ids = []

    results = search_playlists_by_name(name, limit=limit)
    playlist_results.extend(results)

    for result in playlist_results:
        playlist_id = result['id']
        ids.append(playlist_id)

    return ids

def make_random_playlist(name):
    fin_songs = []
    ids = get_random_playlists(name)
    
    for playlist_id in ids:
        fetched_songs = get_random_songs_from_playlist(playlist_id, 5)
        fin_songs.extend(fetched_songs)

    return fin_songs

def get_track_uris(song_names):
    track_uris = []
    for song_name in song_names:
        results = sp.search(q=song_name, type='track', limit=1)
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])
        else:
            print(f"Track '{song_name}' not found on Spotify.")
    
    return track_uris

def create_playlist_and_add_songs(playlist_name, song_uris):
    user_id = sp.me()['id']

    # Create a new playlist
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    # Add songs to the playlist
    sp.playlist_add_items(playlist['id'], song_uris)

    print(f"Playlist '{playlist_name}' created and songs added successfully!")

def remove(string):
    return string.replace(" ", "")




query=input("Enter keyword of which u want a playlist")
query = remove(query)

song_names = [song['name'] for song in make_random_playlist(query)]

# Get the track URIs for each song
song_uris = get_track_uris(song_names)

# Print the obtained track URIs
print("Track URIs:")
for uri in song_uris:
    print(uri)

# Create and add songs to a playlist
create_playlist_and_add_songs(query, song_uris)