from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Iniciar o driver
driver = webdriver.Chrome()

# Acessar a página
url_resultado = "https://www.flashscore.com.br/futebol/espanha/laliga/resultados/"
driver.get(url_resultado)

# Esperar o carregamento
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "event--results")))
time.sleep(10)  # Garantir que tudo carregou

# Pega o container principal
leagues = driver.find_element(By.CLASS_NAME, "container__fsbody") \
                .find_element(By.ID, "live-table") \
                .find_element(By.CLASS_NAME, "event--results") \
                .find_element(By.CLASS_NAME, "sportName.soccer")

# Pegamos todos os elementos que são rodadas ou partidas
elements = leagues.find_elements(By.CSS_SELECTOR, ".event__round, .event__match")

data = []
current_round = None

for el in elements:
    class_list = el.get_attribute("class")
    
    if "event__round" in class_list:
        current_round = el.text.strip()
    
    elif "event__match" in class_list:
        try:
            date_time = el.find_element(By.CLASS_NAME, "event__time").text.strip()
            home_team = el.find_element(By.CLASS_NAME, "event__homeParticipant").text.strip()
            away_team = el.find_element(By.CLASS_NAME, "event__awayParticipant").text.strip()
            home_score = el.find_element(By.CLASS_NAME, "event__score--home").text.strip()
            away_score = el.find_element(By.CLASS_NAME, "event__score--away").text.strip()

            data.append({
                "Rodada": current_round,
                "Data e Hora": date_time,
                "Time da Casa": home_team,
                "Time Visitante": away_team,
                "Placar da Casa": home_score,
                "Placar do Visitante": away_score
            })

        except Exception as e:
            print(f"Erro ao extrair dados da partida: {e}")


for jogo in data:
    print(f'{jogo}\n')

# driver.quit()
with open("laliga/statistics/resultados_laliga.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Dados salvos em 'resultados_laliga.json' com sucesso!")

driver.quit()
