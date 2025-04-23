import json
import time
from selenium import webdriver
import re
from datetime import datetime
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT = "data/raw/statistics/"
PATH = f'{OUTPUT}all_games_statistics.json'
INPUT_URL = "https://www.flashscore.com.br/jogo/futebol/dhHEf26m/#/resumo-de-jogo/estatisticas-de-jogo"

def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado

# def coletar_estatisticas_partidas():
# with open(INPUT_URL, "r", encoding="utf-8") as f:
#     urls = json.load(f)
urls = INPUT_URL

driver = webdriver.Chrome()
todos_os_jogos = []

# for url in urls:
try:
    driver.get(urls)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "container__livetable"))
    )

    date = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text.strip().split(" ")[0]
    data_formatada = datetime.strptime(date, "%d.%m.%Y").strftime("%d/%m/%Y")

    home_team = driver.find_elements(By.CLASS_NAME, "duelParticipant__home")[0].text.strip()
    away_team = driver.find_elements(By.CLASS_NAME, "duelParticipant__away")[0].text.strip()

    id_value = f"{limpar_nome_arquivo(home_team)}_vs_{limpar_nome_arquivo(away_team)}_{data_formatada}".replace(" ", "")

    statistics = driver.find_element(By.CLASS_NAME, "container__livetable") \
                        .find_elements(By.CLASS_NAME, "section")

    estatisticas = {}

    for section in statistics:
        linhas = section.find_elements(By.CLASS_NAME, "wcl-row_OFViZ")
        for linha in linhas:
            home_value = linha.find_element(By.CLASS_NAME, "wcl-homeValue_-iJBW").text.strip()
            category = linha.find_element(By.CLASS_NAME, "wcl-category_7qsgP").text.strip()
            away_value = linha.find_element(By.CLASS_NAME, "wcl-awayValue_rQvxs").text.strip()

            estatisticas[category] = {
                "home_team": home_value,
                "away_team": away_value
            }

    game_stats = {
        "date": data_formatada,
        "id": id_value,
        **estatisticas
    }

    todos_os_jogos.append(game_stats)
    print(f"Coletado: {id_value}")

except Exception as e:
    print(f"Erro ao processar {urls}: {e}")

time.sleep(3)

# with open(PATH, "w", encoding="utf-8") as f:
#     json.dump(todos_os_jogos, f, ensure_ascii=False, indent=4)

print(f"{len(todos_os_jogos)} jogos salvos em: {PATH}")
print(todos_os_jogos)
driver.quit()

