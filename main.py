import re
import json
import requests

# Lista de URLs de los juegos
gog_urls = [
    "https://www.gog.com/en/game/fallout_4_game_of_the_year_edition",
    "https://www.gog.com/en/game/blasphemous",
    "https://www.gog.com/en/game/cyberpunk_2077_ultimate_edition",
    "https://www.gog.com/en/game/manor_lords"
]

# Iterar sobre cada URL
for url in gog_urls:
    # Realizar la solicitud GET a la página web
    result = requests.get(url)

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
        precio = precio_info.get("finalAmount")
        
        # Verificar si se encontró el precio del juego
        if precio:
            print("Precio del juego en", url, ":", precio)
        else:
            print("No se pudo encontrar el precio del juego en", url)
    else:
        print("No se pudo encontrar la parte del HTML que contiene el precio del juego en", url)
