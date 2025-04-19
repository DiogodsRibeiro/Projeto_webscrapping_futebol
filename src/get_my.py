import requests
from bs4 import BeautifulSoup

url_resultado = "https://www.flashscore.com.br/futebol/espanha/laliga/resultados/"

headers = {
    "User-Agent": "Mozilla/5.0"
}
# sao div do html que preciso acessar para buscar os resultados
primeira_camada = "container__fsbody"
segunda_camada = "live-table"
terceira_camada = "loadingOverlay"
quarta_camada = "leagues--static event--leagues results"

response = requests.get(url_resultado, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    leagues = soup.find("div", class_=f'{primeira_camada}') \
                    .find("div", id=f'{segunda_camada}') \
                    .find("div", class_=f'{terceira_camada}') 
                    # .find("div", class_="event event--results") \
                    # .find("div", class_="leagues--static event--leagues results")
    

    print(leagues)