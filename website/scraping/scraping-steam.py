import requests
import requests
from bs4 import BeautifulSoup

def obtener_precio_juego():
    url = "https://store.steampowered.com/app/377160/Fallout_4/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Buscar el elemento que contiene el precio
        precio_element = soup.find("div", class_="game_purchase_price")

        if precio_element:
            # Obtener el precio del juego
            precio = precio_element.get_text().strip()
            return precio
        else:
            return "Precio no encontrado"
    else:
        return "Error al obtener la página:", response.status_code

# Obtener el precio de Fallout 4
precio_juego = obtener_precio_juego()
print("Precio de Fallout 4:", precio_juego)
