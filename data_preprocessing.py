import pandas as pd
import time
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "ENTER_YOUR_ID"
SPOTIPY_CLIENT_SECRET = "ENTER_YOUR_SECRET"
REDIRECT_URI = "http://localhost:3000"
TIMEOUT = 60
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID,
                                                      client_secret = SPOTIPY_CLIENT_SECRET,
                                                      redirect_uri = REDIRECT_URI),
                                                      requests_timeout = TIMEOUT)
song_data = pd.read_csv("C:/Users/ziyue/song/data/Spotify Million Song Dataset_exported.csv")
print(song_data.head())
def get_explicit_label(artist, song):
    try:
        results = sp.search(q="artist:" + artist + " track:" + song, type='track', limit=3)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            retry_after = int(e.response.headers.get('Retry-After', 1))
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after + 1)
        else:
            raise
    #print("result", results,"\n")
    if len(results['tracks']['items'])>0:
        #print(1)
        for t in results['tracks']['items']:
            if t['artists'][0]['name'] == artist:
                #print(2)
                id = t['id']
                label = t['explicit']
                break
            else:
                #print(3)
                id = 'NoMatchingId'
                label = 'NoMatchingLabel'
    else:
        #print(4)
        id = 'NoMatchingId'
        label = 'NoMatchingLabel'
    #print(label)
    return label, id
label = []
list_of_ids = []
artist_start = 0
artist_end = 0
#batch = [(0, 10000), (10000, 20000), (20000, 30000), (30000, 40000), (40000, 50000), (50000, len(song_data))]
batch = [(0, 10000)]
c = 0
#batch = [(10000, 20000)]
#c = 1
#batch = [(20000, 30000)]
#c = 2
#batch = [(30000, 40000)]
#c = 3
#batch = [(40000, 50000)]
#c = 4
#batch = [(50000, 60000)]
#c = 5
for q, tup in enumerate(batch):
    start = tup[0]
    end = tup[1]
    for i in range(start, end):
        l, songid = get_explicit_label(song_data['artist'][i], song_data['song'][i])
        #print(i)
        label.append(l)
        list_of_ids.append(songid)
        if (i % 10 == 0):
            time.sleep(0.5)
            if (i % 100 == 0):
                print("step", i)
        #list_of_ids.append(songid)
    id_series = pd.Series(list_of_ids)
    explicit_series = pd.Series(label)
    song_data['explicit'] = explicit_series
    song_data['id'] = id_series
    #song_data.reset_index()
    fpath = 'C:/Users/ziyue/song/output/song_ids_{f}.csv'.format(f=c)
    song_data.to_csv(fpath, index=False, header=True)
    time.sleep(5.0)
