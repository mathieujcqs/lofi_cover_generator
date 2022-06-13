import json
import spotipy
import requests
from collections import Counter
from spotipy.oauth2 import SpotifyClientCredentials

playlist_ids = ["0vvXsWCC9xrXsKd4FyS8kM", "2qbX2bg93iLsSBmf1OG6Zw", "35xI4hSJ8MdO1xkXwsd56a",
                "4Zi3PGzcLga2wMFn2d5jte", "32hJXySZtt9YvnwcYINGZ0", "5OJs7eATLrvZ2Ea9als3lK",
                "5eDufIy8WtiArgp9aPd9su", "3BH9HNgKSh6E1gVHAWRegN", "71019EDcRamfMmOEEoTdEu",
                "45i3KQ4ENPoZNRYtReXBcU", "3Viw2OdVPeQB5j9JeO6xiF", "5nnhh7IDFWViDWINeh3EhX",
                "6ZUqG9zEynTVKBsgbvVikr", "4hCQNJXRXOQNokU0xnWZGH", "4VN7J0uq62foOhZndwOegy",
                "4x9OtLt7bsmvqktbF0Y0Gm", "3BOxfexQyBa1tsEZ1tJFVQ", "1X4m3caIi1cAXAC5gUO0Ny",
                "3WLDIcG4Cx2UOPy0rbFhQn", "4euMtNSFf0p2lFF2ivAEzb"]

def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


with open("cred.json") as jsonFile:
  jsonObj = json.load(jsonFile)
  jsonFile.close()
  
#Authentication - without user
cid = jsonObj['cid']
secret = jsonObj['cis']

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlists = []

for playlist_id in playlist_ids:
  playlists.extend(get_playlist_tracks(playlist_id))
  
covers_url = []

for playlist in playlists:
  if playlist["track"]["album"]:
    covers_url.append(playlist["track"]["album"]["images"][0]["url"])

duplicates = [k for k,v in Counter(covers_url).items() if v>1]

clean_covers_url = []
for cover_url in covers_url:
  if cover_url not in duplicates:
    clean_covers_url.append(cover_url)
    
covers_url.extend(duplicates)

cover_counter = 1
for url in clean_covers_url:
  img_data = requests.get(covers_url).content
  with open(f"cover_{cover_counter}.jpg", 'wb') as handler:
    handler.write(img_data)
    handler.close()
  cover_counter += 1;
