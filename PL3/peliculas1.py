import requests
from requests import get
from bs4 import BeautifulSoup

url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc"
resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

#print(soup.prettify()) 

peliculasList = soup.find_all("div", class_="lister-item mode-advanced")

for pelicula in peliculasList[0]:
    print(pelicula, end="\n")
    