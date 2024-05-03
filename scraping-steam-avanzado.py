import requests
from bs4 import BeautifulSoup

def obtener_precio_juego_steam(nombre_juego):
    # Reemplaza los espacios en el nombre del juego con signos de más para la URL
    nombre_juego = nombre_juego.replace(" ", "+")
    
    # Construye la URL de búsqueda en Steam
    url_busqueda = f"https://store.steampowered.com/search/?term={nombre_juego}"
    
    # Realiza la solicitud GET a la URL de búsqueda
    response = requests.get(url_busqueda)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Busca el primer enlace de juego en los resultados de búsqueda
        enlace_juego = soup.find("a", class_="search_result_row")["href"]
        
        # Construye la URL completa del juego
        url_juego = f"https://store.steampowered.com{enlace_juego}"
        
        # Realiza una solicitud GET a la URL del juego
        response_juego = requests.get(url_juego)
        print(url_juego)
        
        if response_juego.status_code == 200:
            soup_juego = BeautifulSoup(response_juego.content, "html.parser")
            
            # Busca el elemento que contiene el precio
            precio_element = soup_juego.find("div", class_="game_purchase_price")

            if precio_element:
                # Obtener el precio del juego
                precio = precio_element.get_text().strip()
                return url_juego, precio
            else:
                return url_juego, "Precio no encontrado"
        else:
            return "Error al obtener la página del juego:", response_juego.status_code
    else:
        return "Error al realizar la búsqueda:", response.status_code

# Pedir al usuario el nombre del juego
nombre_juego_usuario = input("Por favor, introduce el nombre del juego en Steam: ")

# Obtener el enlace y el precio del juego
url_juego, precio_juego = obtener_precio_juego_steam(nombre_juego_usuario)
print("Enlace del juego:", url_juego)
print("Precio del juego:", precio_juego)
