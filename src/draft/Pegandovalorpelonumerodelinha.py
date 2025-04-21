from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

driver = webdriver.Chrome()
url = "https://www.flashscore.com.br/futebol/suica/superliga/calendario/"
driver.get(url)

# Espera o container principal carregar
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "live-table")))
time.sleep(10)

# Captura o bloco com todos os jogos
leagues = driver.find_element(By.CLASS_NAME, "container__fsbody") \
                 .find_element(By.ID, "live-table") \
                 .find_element(By.CLASS_NAME, "event--results") \
                 .find_element(By.CLASS_NAME, "event--leagues") \
                 .find_element(By.CLASS_NAME, "sportName.soccer")

# Separar o texto linha a linha
lines = leagues.text.split('\n')

data = []
current_round = None
current_date = None

i = 0
while i < len(lines):
    line = lines[i]

    # Detecta a rodada
    if line.startswith("RODADA"):
        current_round = line

    # Detecta data e hora
    elif re.match(r"\d{2}\.\d{2}\.\s\d{2}:\d{2}", line):
        current_date = line

        # Próximas 4 linhas devem ser: home team, away team, home score, away score
        if i + 4 < len(lines):
            home_team = lines[i+1]
            away_team = lines[i+2]
            home_score = lines[i+3]
            away_score = lines[i+4]

            data.append({
                "Rodada": current_round,
                "Data e Hora": current_date,
                "Time da Casa": home_team,
                "Time Visitante": away_team,
                "Placar da Casa": home_score,
                "Placar do Visitante": away_score
            })

            i += 4  # Pular as 4 linhas que já foram usadas

    i += 1

# Exibir os resultados
for jogo in data:
    print(jogo)

driver.quit()
