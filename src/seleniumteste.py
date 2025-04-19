from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Caminho do ChromeDriver
driver = webdriver.Chrome()

# URL que você quer acessar
url_resultado = "https://www.flashscore.com.br/futebol/espanha/laliga/resultados/"

# Acessar a página
driver.get(url_resultado)

# Esperar até que o elemento da tabela carregue
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "event--results")))

# Esperar mais 10 segundos para garantir que todos os dados carreguem
time.sleep(10)

# Encontrar o elemento específico
leagues = driver.find_element(By.CLASS_NAME, "container__fsbody") \
                 .find_element(By.ID, "live-table") \
                 .find_element(By.CLASS_NAME, "event--results") \
                .find_element(By.CLASS_NAME, "event--leagues") \
                

# Extrair os jogos da página

# DEBUG: Verificar quantas divs existem dentro de leagues
children = leagues.find_elements(By.XPATH, "./div")
print(f"Total de elementos filhos de leagues: {len(children)}")

for idx, child in enumerate(children):
    print(f"\n[{idx}] -> Classe: {child.get_attribute('class')}")
    print(child.text)

# games = leagues.find_elements(By.CLASS_NAME, "sportName soccer")

# data = []

# # Iterar sobre os jogos e extrair as informações
# for game in games:
#     # Extraindo dados do jogo
#     # round_info = game.find_element(By.CLASS_NAME, "event__round event__round--static").text.strip()
#     round_info = driver.find_element(By.CSS_SELECTOR, ".event__round.event__round--static").text.strip()
#     date_time = game.find_element(By.CLASS_NAME, "event__time").text.strip()
#     home_team = game.find_element(By.CLASS_NAME, "wcl-participant_7lPCX event__homeParticipant").text.strip()
#     away_team = game.find_element(By.CLASS_NAME, "wcl-participant_7lPCX event__awayParticipant").text.strip()
#     home_score = game.find_element(By.CLASS_NAME, "wcl-matchRowScore_jcvjd wcl-isFinal_Am7cC event__score event__score--home").text.strip()
#     away_score = game.find_element(By.CLASS_NAME, "wcl-matchRowScore_jcvjd wcl-isFinal_Am7cC event__score event__score--away").text.strip()

#     # Imprimir os resultados estruturados
#     data.append({
#         "Rodada": round_info,
#         "Data e Hora": date_time,
#         "Time da Casa": home_team,
#         "Time Visitante": away_team,
#         "Placar da Casa": home_score,
#         "Placar do Visitante": away_score
#     })


# for entry in data:
#     print(entry)

# # Fechar o driver após terminar
# driver.quit()