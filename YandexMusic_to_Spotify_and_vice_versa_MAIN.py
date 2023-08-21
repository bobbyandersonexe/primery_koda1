def print_name_of_a_track(urlname):
    from yandex_music import Client
    client = Client()

    from urllib.parse import unquote, urlparse
    from pathlib import PurePosixPath
    ids = PurePosixPath(unquote(urlparse(urlname).path)).parts
    album, track = ids[4], ids[2]
    trackID = str(album) + ':' + str(track)

    track_info = client.tracks(trackID)
    title, artist = track_info[0].title, track_info[0].artists_name()[0]

    return artist, title


def get_url_from_spotify_by_artist_and_title(title, artist):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    query = artist + " " + title
    sp_data = sp.search(q=query, type="track", limit=10)

    items = sp_data['tracks']['items']
    if len(items) > 0:
        artist = items[0]['external_urls']['spotify']
        print(artist)
