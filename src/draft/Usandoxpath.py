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

# Encontra todas as rodadas dentro da seção
rounds = leagues.find_elements(By.CLASS_NAME, "event__round.event__round--static")

data = []

# Para cada rodada, pega as partidas associadas
for round_block in rounds:
    try:
        # Captura o nome da rodada (ex: Rodada 32)
        current_round = round_block.text.strip()

        # A próxima parte do código é encontrar todas as partidas associadas à essa rodada
        # Após cada rodada, as partidas estão dentro de divs com a classe 'event__match'.
        # Então, encontramos todas as partidas que estão abaixo dessa rodada

        # Encontrando as partidas que são irmãs (siblings) da rodada
        next_sibling = round_block.find_elements(By.XPATH, "following-sibling::div[contains(@class, 'event__match')]")

        # Para cada partida dentro dessa rodada
        for match in next_sibling:
            try:
                # Captura os dados da partida
                date_time = match.find_element(By.CLASS_NAME, "event__time").text.strip()
                home_team = match.find_element(By.CLASS_NAME, "event__homeParticipant").text.strip()
                away_team = match.find_element(By.CLASS_NAME, "event__awayParticipant").text.strip()
                home_score = match.find_element(By.CLASS_NAME, "event__score--home").text.strip()
                away_score = match.find_element(By.CLASS_NAME, "event__score--away").text.strip()

                # Adiciona os dados no resultado
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

    except Exception as e:
        print(f"Erro ao capturar a rodada: {e}")

# Exibe o resultado final
for jogo in data:
    print(jogo)

driver.quit()
