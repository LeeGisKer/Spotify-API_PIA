from flask import Flask, jsonify, request
from collections import defaultdict

import matplotlib.pyplot as plt
import requests
import re
import json

from graficas import create_charts
from scripts import main

app = Flask(__name__)

client_id = 'de6e57a5354c491a96ec3b6ff0b09ca8'
client_secret = 'b8d8405d57764a03a9b83cbcd1b42e9e'


def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    return auth_response.json().get('access_token')
    

def clean_data(data):
    tracks = data.get('tracks', {}).get('items', [])
    cleaned_data = []

    for item in tracks:
        track_info = item.get('track', {})
        cleaned_data.append({
            'track_name': track_info.get('name'),
            'artist_name': [artist['name'] for artist in track_info.get('artists', [])],
            'album_name': track_info.get('album', {}).get('name'),
            'release_date': track_info.get('album', {}).get('release_date'),
            'popularity': track_info.get('popularity'),
            'duration_ms': track_info.get('duration_ms'),
        })
        

    
    return cleaned_data




@app.route('/get_playlist_data', methods=['GET'])
def get_playlist_data():
    playlist_id = request.args.get('playlist_id')
    
    if not re.match(r'^[a-zA-Z0-9]{22}$', playlist_id):
        return jsonify({'error': 'Invalid playlist ID format'}), 400

    access_token = get_spotify_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch playlist data'}), response.status_code

    data = response.json()
    cleaned_data = clean_data(data)
    
    structured_data = {
        "playlist": {
            "name": data.get("name"),
            "description": data.get("description"),
            "total_tracks": data.get("tracks", {}).get("total")
        },
        "tracks": cleaned_data
    }
    
    with open('playlist_data.json', 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=4)
        
    return jsonify(structured_data)


create_charts()

main()

if __name__ == '__main__':
    app.run(debug=True)