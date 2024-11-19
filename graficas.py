import numpy as np
import json
import matplotlib.pyplot as plt

from collections import defaultdict
from scripts import load_data, datavisual, artistas_mas_populares


def histograma_popularidad(data):
    popularity, _ = datavisual(data)
    plt.hist(popularity, bins=10, edgecolor='black')
    plt.title('Distribución de Popularidad de Canciones')
    plt.xlabel('Popularidad')
    plt.ylabel('Número de Canciones')
    plt.show()
    
def histograma_duracion(data):
    _, durations = datavisual(data)
    plt.hist(durations, bins=10, edgecolor='black')
    plt.title('Distribución de la Duración de Canciones')
    plt.xlabel('Duración (minutos)')
    plt.ylabel('Número de Canciones')
    plt.show()
    
def pastel(data):
    popularidad_artistas = defaultdict(int)
    for track in data['tracks']:
        for artist in track['artist_name']:
            popularidad_artistas[artist] += track['popularity']
    
    top_artistas = sorted(popularidad_artistas.items(), key=lambda x: x[1], reverse=True)[:5]
    labels = [artist[0] for artist in top_artistas]
    sizes = [artist[1] for artist in top_artistas]
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Top 5 Artistas con Mayor Popularidad')
    plt.show()
    
def lineal(data):
    _, durations = datavisual(data)
    indices = list(range(len(durations)))
    
    plt.plot(indices, durations, marker='o')
    plt.title('Distribución de la Duración de Canciones')
    plt.xlabel('Canción')
    plt.ylabel('Duración (minutos)')
    plt.grid()
    plt.show()


    
def top_artistas(data,top_n=10):
    artista_mas_popular, popularidad, artista_mas_repetido, frecuencia = artistas_mas_populares(data)
    popularidad_artistas = defaultdict(list)
    
    for track in data['tracks']:
        for artist in track['artist_name']:
            popularidad_artistas[artist].append(track['popularity'])
            
    promedio_popularidad = {artist: np.mean(popularities) for artist, popularities in popularidad_artistas.items()}
    sorted_artists = sorted(promedio_popularidad.items(), key=lambda x: len(popularidad_artistas[x[0]]), reverse=True)
    top_artists = sorted_artists[:top_n]
    
    artists = [artist for artist, _ in top_artists]
    frequencies = [len(popularidad_artistas[artist]) for artist, _ in top_artists]
    avg_popularities = [promedio_popularidad[artist] for artist, _ in top_artists]
    
    fig, ax1 = plt.subplots()
    ax1.bar(artists, frequencies, color='b', alpha=0.6, label='Frecuencia')
    ax1.set_xlabel('Artistas')
    ax1.set_ylabel('Frecuencia', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(artists, avg_popularities, color='r', marker='o', label='Popularidad Promedio')
    ax2.set_ylabel('Popularidad Promedio', color='r')
    ax2.tick_params(axis='y', labelcolor='r')


    plt.title(f'Top {top_n} Artistas Más Frecuentes y su Popularidad Promedio')
    fig.tight_layout()
    plt.show()
    
def create_charts():
    data = load_data()
    histograma_popularidad(data)
    histograma_duracion(data)
    top_artistas(data, top_n=10)
    pastel(data)
    lineal(data)
    
if __name__ == "__main__":
    create_charts()



    







