from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

app = Flask(__name__, template_folder='templates')
app.secret_key = "Game_Wallet1234"
# isigamewallet

# Global vars
Steam = "https://store.steampowered.com/search/?term="
IG = "https://www.instant-gaming.com/fr/rechercher/?gametype=games&query="
G2A = "https://www.g2a.com/es/category/gaming-c1?f[product-kind][0]=10&query="

# Function to return JSON object
def ReturnElem(title=None, picture_url=None, price=None, opinion=None, link=None):
    game_info = {
        'title': title[:16] if title else "-",
        'opinion': opinion if opinion else "-",
        'price': price if price else "-",
        'link': link if link else "-",
        'picture_url': picture_url if picture_url else "-"
    }
    return game_info

def ScrappingSteam(userSearch):
    url = Steam + userSearch
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        result = soup.find('a', class_='search_result_row')
        if not result:
            raise ValueError("No results found")

        title = result.find('span', class_='title').text if result.find('span', class_='title') else "No title"
        picture_url = result.img['src'] if result.img else "No image"
        opinion_tag = result.find("span", {"class": "search_review_summary positive"})
        opinion = opinion_tag["data-tooltip-html"].split("<br>")[0] if opinion_tag else "No opinion"

        # Find the price element
        price_element = result.find('div', class_='search_price')
        if not price_element:
            price_element = result.find('div', class_='discount_final_price')

        # Extract the price
        price = price_element.text.strip().replace('\r\n', '').replace('\n', '').replace('\t', '') if price_element else "No price"

        link = result['href'] if result['href'] else "No link"
    except Exception as e:
        print(f"Error scraping Steam: {e}")
        title = picture_url = price = opinion = link = "No data"
    
    return ReturnElem(title, picture_url, price, opinion, link)

# Function for Instant Gaming scraping
def ScrappingIG(userSearch):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    IG_url = IG + userSearch.replace(" ", "%20")
    driver.get(IG_url)
    try:
        titles = driver.find_elements(By.CLASS_NAME, "title")
        pictures = driver.find_elements(By.CLASS_NAME, "picture")
        prices = driver.find_elements(By.CLASS_NAME, "price")
        
        if len(titles) > 4 and len(pictures) > 0 and len(prices) > 1:
            title = titles[4].get_attribute('innerHTML')
            picture_url = pictures[0].get_attribute('src')
            # Utilizar un método más robusto para obtener el precio
            price_element = prices[1]
            # Limpiar el texto del precio para obtener solo el número
            price_text = price_element.text.strip()
            # Si el precio tiene una etiqueta <spam>, eliminarla
            price = price_text.split("<")[0]
            opinion = "No opinion"
            link = IG_url
        else:
            raise IndexError("Not enough elements found")
    except Exception as e:
        print(f"Error scraping Instant Gaming: {e}")
        title = picture_url = price = opinion = link = "No data"
    finally:
        driver.quit()
    
    return ReturnElem(title, picture_url, price, opinion, link)


# SIN IMPLEMENTAR PERO FUNCIONAL
# Function for G2A scraping
def ScrappingG2A(userSearch):
    # Inicialización del navegador Chrome
    driver = webdriver.Chrome()
    
    # Construcción de la URL con la búsqueda del usuario
    G2A_url = G2A + userSearch.replace(" ","%20")
    driver.get(G2A_url)

    try:
        # Extracción del título del juego
        title = driver.find_element(By.XPATH, "//h3/a").text
    except:
        title = " - "

    try:
        # Extracción de la URL de la imagen del juego
        picture_url = driver.find_element(By.XPATH, "//a[contains(@class, 'sc-jQAxuV')]/img").get_attribute('src')
    except:
        picture_url = " - "

    try:
        # Extracción del precio del juego
        price = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-iqAclL sc-crzoAE dJFpVb eqnGHx sc-bqGGPW gjCrxq')]").text
    except:
        price = " - "
    
    # La opinión no parece estar disponible en el código proporcionado, así que se establece como "-"
    opinion = "No opinion"
    
    # La URL se establece como la URL de la búsqueda en G2A
    link = G2A_url
    
    # Cierre de la ventana del navegador
    driver.close()
    
    # Devuelve la información obtenida
    print (title, picture_url, price, opinion, link)
    return ReturnElem(title, picture_url, price, opinion, link) 



# Function for EpicGames scraping
def ScrappingEpicGames(userSearch):
    # URL de la API GraphQL de Epic Games
    url = "https://graphql.epicgames.com/graphql"
    
    # URL base para buscar juegos en la tienda de Epic Games
    search_url = f"https://store.epicgames.com/en-US/browse?q={userSearch.replace(' ', '%20')}&sortBy=relevancy"

    # Consulta GraphQL para buscar un juego en la tienda de Epic Games
    query = """
    query searchStoreQuery(
      $allowCountries: String
      $category: String
      $namespace: String
      $itemNs: String
      $sortBy: String
      $sortDir: String
      $start: Int
      $tag: String
      $releaseDate: String
      $withPrice: Boolean = true
      $keywords: String
    ) {
      Catalog {
        searchStore(
          allowCountries: $allowCountries
          category: $category
          count: 1
          country: "ES"
          keywords: $keywords
          namespace: $namespace
          itemNs: $itemNs
          sortBy: $sortBy
          sortDir: $sortDir
          releaseDate: $releaseDate
          start: $start
          tag: $tag
        ) {
          elements {
            title
            keyImages {
              type
              url
            }
            productSlug
            urlSlug
            url
            price(country: "ES") @include(if: $withPrice) {
              totalPrice {
                fmtPrice(locale: "en-ES") {              
                  discountPrice             
                }
              }
            }
            customAttributes {
              key
              value
            }
          }
        }
      }
    }
    """

    # Parámetros de la consulta GraphQL
    params = {
        "operationName": "searchStoreQuery",
        "variables": {
            "allowCountries": None,
            "category": None,
            "namespace": None,
            "itemNs": None,
            "sortBy": None,
            "sortDir": None,
            "start": None,
            "tag": None,
            "releaseDate": None,
            "withPrice": True,
            "keywords": userSearch
        },
        "query": query
    }

    try:
        # Realizar la solicitud POST a la API GraphQL de Epic Games
        response = requests.post(url, json=params)
        # Obtener el JSON de la respuesta
        json_data = response.json()

        # Extraer la información del juego desde el JSON
        game_info = json_data["data"]["Catalog"]["searchStore"]["elements"][0]
        title = game_info["title"]
        picture_url = None
        for image in game_info["keyImages"]:
            if image["type"] == "OfferImageWide":
                picture_url = image["url"]
                break
        price = game_info["price"]["totalPrice"]["fmtPrice"]["discountPrice"]

    except Exception as e:
        title = " - "
        picture_url = " - "
        price = " - "

    # Establecer la opinión como "no opinion"
    opinion = "no opinion"

    # URL de la tienda de Epic Games
    link = search_url
    
    # Devolver la información obtenida
    return ReturnElem(title, picture_url, price, opinion, link)
  

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling game search requests
@app.route('/search', methods=['GET'])
def search_view():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    steam_data = ScrappingSteam(query)
    ig_data = ScrappingIG(query)
    EpicGames_data = ScrappingEpicGames(query)
    #G2A_data = ScrappingG2A(query)

    results = [steam_data, ig_data, EpicGames_data] #añadir G2A_data

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
