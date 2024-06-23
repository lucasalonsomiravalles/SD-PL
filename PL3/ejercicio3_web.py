import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.atptour.com/es/rankings/singles"
resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

tenistasPandas = []
tenistasList = soup.find_all("tr")

for tenista in tenistasList:
    ranking = ranking.find("td", class_="rank-cell border-left-4 border-right-dash-1").text
    
    nombre = tenista.find("td", class_="player-cell border-left-dash-1 border-right-dash-1")
    nombre = nombre.find("span", class_="player-cell-wrapper").text

    edad = edad.find("td", class_="age-cell border-left-dash-1 border-right-4").text

    puntos = tenista.find("td", class_="points-cell border-right-dash-1")
    puntos = puntos.find("a", class_="rankings-breakdown").text

    tenistasPandas.append({'Ranking':ranking, 'Nombre':nombre, 'Edad':edad, 'Puntos':puntos})

tenistas_dataFrame = pd.DataFrame(tenistasPandas)

tenistas_dataFrame.to_csv('tenistas.csv', index=True)
print('CSV creado correctamente')

tenistas_dataFrame.to_json('tenistas.json', orient='records')
print('JSON creado correctamente')

tenistas_dataFrame.to_excel('tenistas.xlsx', index=False)
print('Excel creado correctamente')