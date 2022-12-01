import json
import spotipy
import requests
from collections import Counter
from spotipy.oauth2 import SpotifyClientCredentials

with open("cred.json") as jsonFile:
  jsonObj = json.load(jsonFile)
  jsonFile.close()
  
#Authentication - without user
cid = jsonObj['cid']
secret = jsonObj['cis']

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_ids(offsets):
  items = []
  for offset in offsets:
    results = sp.search(q="lofi, study, beats, chill", limit=50, type="playlist", offset=offset)
    items.extend([item['id'] for item in results['playlists']['items']])
  return items

def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

playlists = []
for playlist_id in get_playlist_ids([0,50]):
  playlists.extend(get_playlist_tracks(playlist_id))

print('playlist : ', len(playlists))

covers_url = []
for playlist in playlists:
  if len(playlist["track"]["album"]['images']) > 0:
    covers_url.append(playlist["track"]["album"]["images"][0]["url"])

print('covers_url : ', len(covers_url))

duplicates = [key for key, value in Counter(covers_url).items() if value > 1]

print('duplicates : ', len(duplicates))

clean_covers_url = []
for cover_url in covers_url:
  if cover_url not in duplicates:
    clean_covers_url.append(cover_url)
    
clean_covers_url.extend(duplicates)
print('clean_covers_url : ', len(clean_covers_url))

for i in range(len(clean_covers_url)):
  img_data = requests.get(clean_covers_url[i]).content
  with open(f"covers/cover_{i+1}.jpg", 'wb') as handler:
    handler.write(img_data)
    handler.close()
    