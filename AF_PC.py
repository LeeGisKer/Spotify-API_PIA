from collections import defaultdict

import matplotlib.pyplot as plt
import requests
import re
import json

with open('playlist_data.json') as f:
    data = json.load(f)

popularidad_artistas = defaultdict(list)

for track in data['tracks']:
    for artist in track['artist_name']:
        popularidad_artistas[artist].append(track['popularity'])

promedio_popularidad = {artist: sum(popularities) / len(popularities) for artist, popularities in popularidad_artistas.items()}

filtro_artists = sorted(promedio_popularidad.items(), key=lambda x: len(popularidad_artistas[x[0]]), reverse=True)

top_artistas = filtro_artists[:10]
print("Top 10 artistas con mayor cantidad de canciones en la playlist:")
for artist, avg_popularity in top_artistas:
    print(f"{artist}: Frecuencia - {len(popularidad_artistas[artist])}, Popularidad Promedio - {avg_popularity:.2f}")
        
artists = [artist for artist, _ in top_artistas]
frequencies = [len(popularidad_artistas[artist]) for artist, _ in top_artistas]
avg_popularities = [avg_pop for _, avg_pop in top_artistas]


