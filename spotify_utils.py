import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
import random
import os
import tempfile

# Spotify credentials and scopes
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
CACHE_PATH = os.path.join(tempfile.gettempdir(), '.spotify_token_cache')

def get_spotify_client():
    """
    Authenticate the user and return a Spotify client instance.
    Uses Spotipy's SpotifyOAuth helper for OAuth flow.
    """
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH
    ))

def get_user_playlists(sp):
    """
    Fetch all playlists that the current user can see.
    Returns a list of playlist dicts.
    """
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return playlists

def get_tracks_grouped_by_album(sp, playlist_id):
    """
    Given a playlist ID, fetch all tracks grouped by their album.
    Returns a dictionary: {album_name: [tracks_in_order]}
    This helps us keep the song order within each album.
    """
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        tracks.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break

    albums = defaultdict(list)
    for item in tracks:
        track = item['track']
        if not track or not track['album'] or not track['album']['id']: # skip local or unavailable tracks
            continue
        album_id = track['album']['id']
        albums[album_id].append(track)

    return list(albums.values())

def shuffle_albums(album_groups):
    """
    Shuffle the order of albums but keep the tracks inside each album in original order.
    Returns a flat list of tracks in shuffled album order.
    """
    random.shuffle(album_groups)
    shuffled_tracks = [track for album in album_groups for track in album] # add tracks in original order
    return shuffled_tracks

def create_road_trip_playlist(sp, user_id, original_playlist_name, tracks):
    """
    Create a new playlist named "[original_playlist_name] (Road Trip Shuffle)".
    Add the shuffled tracks to the new playlist.
    Returns the URL of the created playlist.
    """
    new_name = f"{original_playlist_name} (Road Trip Shuffle)"
    new_playlist = sp.user_playlist_create(user=user_id, name=new_name)
    track_uris = [track['uri'] for track in tracks]

    # Spotify API limits adding max 100 tracks per request
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(new_playlist['id'], track_uris[i:i+100])
    return new_playlist['external_urls']['spotify']
