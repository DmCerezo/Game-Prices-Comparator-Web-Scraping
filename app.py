from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

app = Flask(__name__, template_folder='templates')
app.secret_key = "Game_Wallet1234"

# Global vars
Steam = "https://store.steampowered.com/search/?term="
IG = "https://www.instant-gaming.com/fr/rechercher/?gametype=games&query="
GOG = "https://www.gog.com/en/games?query="

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

# Function for Steam scraping
def ScrappingSteam(userSearch):
    url = Steam + userSearch
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('a', class_='search_result_row')
    try:
        title = result.find('span', class_='title').text
        picture_url = result.img['src']
        opinion = soup.find("span", {"class": "search_review_summary positive"})["data-tooltip-html"].split("<br>")[0]
        price = result.find('div', class_='search_price').text.replace(' ', '').replace('\r\n', '')
        if price.count("€") > 1:
            prices = price.split("€")
            price = prices[1] + "€"
    except AttributeError:
        title = " - "
        picture_url = " - "
        price = " - "
        opinion = " - "
        url = " - "
    return ReturnElem(title, picture_url, price, opinion, url)

# Function for Instant Gaming scraping
def ScrappingIG(userSearch):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    IG_url = IG + userSearch.replace(" ", "%20")
    driver.get(IG_url)
    try:
        title = driver.find_elements(By.CLASS_NAME, "title")[4].get_attribute('innerHTML')
        picture_url = driver.find_elements(By.CLASS_NAME, "picture")[0].get_attribute('src')
        price = driver.find_elements(By.CLASS_NAME, "price")[1].get_attribute('innerHTML')
        opinion = " - "
        url = IG_url
    except IndexError:
        title = " - "
        picture_url = " - "
        price = " - "
        opinion = " - "
        url = " - "
    driver.quit()
    return ReturnElem(title, picture_url, price, opinion, url)

# Function for GOG scraping
def ScrappingGOG(userSearch):
    GOG_url = GOG + userSearch.replace(" ", "%20")
    request_text = requests.get(GOG_url).text
    htmlpage = BeautifulSoup(request_text, "html.parser")
    try:
        title = htmlpage.find_all(class_="product-tile__title")[0].get('title')
        picture_url = '0'
        price = htmlpage.find_all(class_="final-value")[0].text
        opinion = '0'
    except IndexError:
        title = " - "
        picture_url = " - "
        price = " - "
        opinion = " - "
        GOG_url = " - "
    return ReturnElem(title, picture_url, price, opinion, GOG_url)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling game search requests
@app.route('/search', methods=['GET', 'POST'])
def search_view():
    userSearch = request.form['q']
    if userSearch:
        table = [
            ScrappingSteam(userSearch),
            ScrappingIG(userSearch),
            ScrappingGOG(userSearch)
        ]

        print(table)  # Print data to the Flask server terminal

    return jsonify(table)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
