import re
import json
import requests

def obtener_precio_fallout_4():
    # URL del juego Fallout 4 en GOG
    fallout_4_url = "https://www.gog.com/en/game/fallout_4_game_of_the_year_edition"

    # Realizar la solicitud GET a la página web
    result = requests.get(fallout_4_url)

    # Obtener el contenido HTML de la página web
    content = result.text

    # Patrón de expresión regular para encontrar la parte del HTML que contiene el precio del juego
    patron = r'"price":{([^}]+)}'
    precio_match = re.search(patron, content)

    # Verificar si se encontró la parte del HTML que contiene el precio del juego
    if precio_match:
        # Extraer la parte del HTML que contiene el precio del juego
        precio_info_html = "{" + precio_match.group(1) + "}"
        
        # Convertir la parte del HTML a un objeto JSON
        precio_info = json.loads(precio_info_html)
        
        # Obtener el precio final del juego del objeto JSON
        precio_fallout_4 = precio_info.get("finalAmount")
        return precio_fallout_4
    else:
        return None  # En caso de que no se encuentre el precio del juego

# Obtener el precio de Fallout 4
precio_fallout_4 = obtener_precio_fallout_4()

# Guardar el precio en un archivo JSON
if precio_fallout_4 is not None:
    with open('precio_fallout_4.json', 'w') as file:
        json.dump({'precio_fallout_4': precio_fallout_4}, file)
