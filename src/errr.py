from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Iniciar o driver do Chrome
driver = webdriver.Chrome()

# Acessar a página de resultados
url_resultado = "https://www.flashscore.com.br/futebol/espanha/laliga/resultados/"
driver.get(url_resultado)

# Espera o carregamento da tabela
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "event--results")))
time.sleep(10)  # Espera extra só pra garantir

# Localiza a seção da LaLiga
leagues = driver.find_element(By.CLASS_NAME, "container__fsbody") \
                .find_element(By.ID, "live-table") \
                .find_element(By.CLASS_NAME, "event--results") \
                .find_element(By.CLASS_NAME, "sportName.soccer")

# Pegamos a rodada atual fora das partidas (ela aparece antes dos jogos)
try:
    current_round = leagues.find_element(By.CLASS_NAME, "event__round.event__round--static").text.strip()
except:
    current_round = "Rodada não encontrada"

# Pegamos todas as partidas
matches = leagues.find_elements(By.CLASS_NAME, "event__match")

data = []

for match in matches:
    try:
        date_time = match.find_element(By.CLASS_NAME, "event__time").text.strip()
        home_team = match.find_element(By.CLASS_NAME, "event__homeParticipant").text.strip()
        away_team = match.find_element(By.CLASS_NAME, "event__awayParticipant").text.strip()
        home_score = match.find_element(By.CLASS_NAME, "event__score--home").text.strip()
        away_score = match.find_element(By.CLASS_NAME, "event__score--away").text.strip()

        data.append({
            "Rodada": current_round,
            "Data e Hora": date_time,
            "Time da Casa": home_team,
            "Time Visitante": away_team,
            "Placar da Casa": home_score,
            "Placar do Visitante": away_score
        })

    except Exception as e:
        print(f"Erro ao extrair dados de uma partida: {e}")

# Exibe o resultado final
for jogo in data:
    print(jogo)

driver.quit()
