import requests
from requests import get
from bs4 import BeautifulSoup

url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc"
resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

#print(soup.prettify()) 

peliculasList = soup.find_all("div", class_="lister-item mode-advanced")

for pelicula in peliculasList:
    titulo = pelicula.find("h3", class_="lister-item-header")
    titulo = titulo.find("a").text

    duracion = pelicula.find("p", class_="text-muted")
    duracion = duracion.find("span", class_="runtime").text

    puntuacion = pelicula.find("div", class_="lister-item-content")
    puntuacion = puntuacion.find("div", class_="ratings-bar")
    puntuacion = puntuacion.find("div", {"class": "inline-block ratings-imdb-rating", "name":"ir", "data-value": True})
    puntuacion = puntuacion.find("strong").text

    director =pelicula.find("div", class_="lister-item-content")
    director=director.find("p",class_="")
    director=director.find("a").text
    if pelicula.find("span", class_="metascore"):
        metascore=pelicula.find("span", class_="metascore").text
    else:
        metascore = "-----"
    print("-------------------")
    print("Titulo:")
    print(titulo,"\n")
    print("Duracion:")
    print(duracion.split()[0],"\n")
    print("Puntuacion:")
    print(puntuacion,"\n")
    print("Nombre del director:")
    print(director,"\n")
    print("Metascore:")
    print(metascore)
    print("-------------------")
    print("\n")