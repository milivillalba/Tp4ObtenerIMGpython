import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# Aquí voy a almacenar la URL del sitio web del cual quiero obtener las imágenes, en este caso, usaré MercadoLibre
url = 'https://www.mercadolibre.com.ar/c/autos-motos-y-otros#menu=categories'

# Función para obtener las imágenes de MercadoLibre
def Obtener_Img(url):
    # Creo una carpeta para almacenar las imágenes
    crear_carpeta_img()

    # Realizo la solicitud GET para obtener las imágenes y sus atributos src
    response = requests.get(url)

    # Verificar si la solicitud a la URL fue exitosa
    if response.status_code == 200:
        # Si fue exitosa, parseo el contenido HTML usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentro todas las etiquetas <img> con la clase "dynamic-carousel__img"
        imagenes = soup.find_all('img', class_="dynamic-carousel__img")

        # Recorro cada imagen
        for img in imagenes:
            # Obtengo la URL de la imagen
            img_url = img.get('data-src')
            # Verifico si la URL es válida y si la imagen es de un formato permitido
            if img_url and img_url.startswith('http') and img_url.lower().endswith(('.png', '.jpg', '.webp')):
                # Descargo la imagen
                descargar_img(img_url)
            else:
                print("Imagen no válida:", img_url)
    else:
        print(f"Error al obtener la página: {response.status_code}")

# Función para crear la carpeta donde se almacenarán las imágenes
def crear_carpeta_img():
    # Si no existe la carpeta imágenes que la cree
    if not os.path.exists('imagenes'):
        os.makedirs('imagenes')

# Función para descargar una imagen dada la URL y guardarla en la carpeta imágenes
def descargar_img(img_url):
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(os.path.join('imagenes', os.path.basename(urlparse(img_url).path)), 'wb') as f:
                f.write(response.content)
                print("Imagen descargada:", img_url)
    except Exception as e:
        print("Error al descargar la imagen:", img_url)
        print(e)

# Llamo a la función para obtener las imágenes de MercadoLibre
Obtener_Img(url)