import pandas as pd
import time
import spotipy
from IPython.display import display
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
song_processed = pd.read_csv("C:/Users/ziyue/song/output/data/song_data_with_id_explicit_cleaned.csv")
#display(song_processed.tail())

features = {}
all_track_ids = list(song_processed['id'])
lenlist = len(all_track_ids)
start = 0
num_tracks = 100
cnt = 0
while start < lenlist:
    tracks_batch = all_track_ids[start:start+num_tracks]
    features_batch = sp.audio_features(tracks_batch)
    time.sleep(0.1)
    cnt+=1
    print("batch number", cnt)
    #print("start", start, "dict", features_batch)
    features.update({ track_id : track_features
                 for track_id, track_features in zip(tracks_batch, features_batch) })
    #if (start == num_tracks):
    start += num_tracks
song_ids = []
frames = []
for song_id, d in features.items():
    if not d:
        continue
    song_ids.append(song_id)
    frame = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in d.items()]))
    #print(frame)
    frames.append(frame)
    #df = pd.DataFrame(frame)
df = pd.concat(frames)
display("shape is", df.shape)
display(df.head())
display(df.columns)
display(df['id'].tail())
display(song_processed['id'].tail())
fpath = 'C:/Users/ziyue/song/output/features.csv'
df.to_csv(fpath, index=False, header=True)
#print(features)

