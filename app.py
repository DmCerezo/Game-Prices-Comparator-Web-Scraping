from flask import Flask, render_template
import re
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates')

# Obtener precio de Fallout 4 en Steam
def obtener_precio_fallout_4_STEAM():
    url = "https://store.steampowered.com/app/377160/Fallout_4/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        precio_element = soup.find("div", class_="game_purchase_price")
        
        if precio_element:
            precio = precio_element.get_text().strip()
            return precio
        else:
            return "Precio no encontrado"
    else:
        return f"Error al obtener la página: {response.status_code}"

# Obtener precio de Fallout 4 en GOG
def obtener_precio_fallout_4_GOG():
    url = "https://www.gog.com/en/game/fallout_4_game_of_the_year_edition"
    result = requests.get(url)
    
    if result.status_code == 200:
        content = result.text
        patron = r'"price":{([^}]+)}'
        precio_match = re.search(patron, content)
        
        if precio_match:
            precio_info_html = "{" + precio_match.group(1) + "}"
            precio_info = json.loads(precio_info_html)
            precio_fallout_4_GOG = precio_info.get("finalAmount")
            return precio_fallout_4_GOG
        else:
            return "Precio no encontrado"
    else:
        return f"Error al obtener la página: {result.status_code}"

@app.route('/')
def index():
    precio_fallout_4_steam = obtener_precio_fallout_4_STEAM()
    precio_fallout_4_gog = obtener_precio_fallout_4_GOG()
    return render_template('index.html', precio_fallout_4_steam=precio_fallout_4_steam, precio_fallout_4_gog=precio_fallout_4_gog)

@app.route('/buscar_juegos')
def buscar():
    return render_template('buscar_juegos.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/juego/<nombre>')
def juego(nombre):
    return f"Este es el juego {nombre}"

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=8080, debug=True)
