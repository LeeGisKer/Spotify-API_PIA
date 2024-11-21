from openpyxl import Workbook
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt
import os

from graficas import histograma_popularidad, histograma_duracion, pastel, lineal, top_artistas, graficas_imagenes
from scripts import load_data, datavisual


def crearexcel():
    data = load_data()
    graficas_imagenes(data)

    wb = Workbook()
    ws = wb.active
    ws.title = "Graficas de Playlist"

    graph_folder = 'graficas'
    images = [
        ("Histograma de Popularidad", f"{graph_folder}/histograma_popularidad.png"),
        ("Histograma de Duración", f"{graph_folder}/histograma_duracion.png"),
        ("Gráfica de Pastel", f"{graph_folder}/pastel.png"),
        ("Gráfica Lineal", f"{graph_folder}/lineal.png"),
        ("Top Artistas", f"{graph_folder}/topartistas.png"),
    ]

    row = 1
    for title, path in images:
        ws.cell(row=row, column=1, value=title)
        row += 1

        if os.path.exists(path):
            img = Image(path)
            ws.add_image(img, f'A{row}')
            row += 20
        else:
            print(f"Warning: {path} does not exist!")

    excel_file = "Graficas.xlsx"
    wb.save(excel_file)
    print(f"Archivo Excel '{excel_file}' creado con éxito.")

if __name__ == "__main__":
    crearexcel()