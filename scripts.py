import json 
import re
import numpy as np

from collections import defaultdict
from statistics import mean, median, stdev

def load_data(filename='playlist_data.json'):
    with open(filename,'r',encoding='utf-8') as f:
        data = json.load(f)
    return data

def valiciondatos(data):
    for track in data['tracks']:
        release_date = track.get('release_date')
        if not re.match(r'^\d{4}(-\d{2})?(-\d{2})?$', release_date):
            print(f"fecha no valida: [{release_date}]")
            
        nombretrack = track.get('track_name')
        if not isinstance(nombretrack, str):
            print(f"nombre no valido: [{nombretrack}]")
            
def datavisual(data):
    popularity = [track['popularity'] for track in data['tracks']]
    duracion = [track['duration_ms'] / 60000 for track in data['tracks']]
    return popularity, duracion

def estadisticas(popularity, duracion):
    stats = {
        'popularidad_promedio': mean(popularity),
        'popularidad_mediana': median(popularity),
        'popularidad_std_dev': stdev(popularity),
        'duracion_promedio': mean(duracion),
        'duracion_mediana': median(duracion),
        'duracion_std_dev': stdev(duracion)
    }
    return stats

def artistas_mas_populares(data):
    popularidad_artistas = defaultdict(list)
    
    for track in data['tracks']:
        for artist in track['artist_name']:
            popularidad_artistas[artist].append(track['popularity'])
            
    promedio_popularidad = {artist: mean(popularities) for artist, popularities in popularidad_artistas.items()}
    
    artista_mas_popular = max(promedio_popularidad, key=promedio_popularidad.get)
    
    artista_mas_repetido = max(popularidad_artistas, key=lambda artist: len(popularidad_artistas[artist]))
    
    return artista_mas_popular, promedio_popularidad[artista_mas_popular], artista_mas_repetido, len(popularidad_artistas[artista_mas_repetido])


def main():
    data = load_data()
    valiciondatos(data)
    popularity, duracion = datavisual(data)
    stats = estadisticas(popularity, duracion)
    
    print("Estadisticas:")
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")
        
    artista_mas_popular, popularidad, artista_mas_repetido, frecuencia = artistas_mas_populares(data)
        
if __name__ == "__main__":
    main()

