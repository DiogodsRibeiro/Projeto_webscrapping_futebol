from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from  datetime import datetime
from selenium.common.exceptions import NoSuchElementException



driver = webdriver.Chrome()

url_resultado = "https://www.flashscore.com.br/futebol/espanha/laliga/resultados/"
driver.get(url_resultado)

ano_atual = datetime.now().year

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "event--results")))
time.sleep(10)  

while True:
    try:
        mostrar_mais = driver.find_element(By.CLASS_NAME, "event__more")
        driver.execute_script("arguments[0].click();", mostrar_mais)
        time.sleep(8)
    except NoSuchElementException:
        break

season = driver.find_element(By.CLASS_NAME, "heading__info").text.strip()

campeonato = driver.find_element(By.CLASS_NAME, "heading__title")\
                   .find_element(By.CLASS_NAME, "heading__name").text.strip()


leagues = driver.find_element(By.CLASS_NAME, "container__fsbody") \
                .find_element(By.ID, "live-table") \
                .find_element(By.CLASS_NAME, "event--results") \
                .find_element(By.CLASS_NAME, "sportName.soccer")

elements = leagues.find_elements(By.CSS_SELECTOR, ".event__round, .event__match")

data = []
current_round = None

for el in elements:
    class_list = el.get_attribute("class")
    
    if "event__round" in class_list:
        current_round = el.text.strip()
    
    elif "event__match" in class_list:
        try:
            date_time_raw = el.find_element(By.CLASS_NAME, "event__time").text.strip()
            home_team = el.find_element(By.CLASS_NAME, "event__homeParticipant").text.strip()
            away_team = el.find_element(By.CLASS_NAME, "event__awayParticipant").text.strip()
            home_score = el.find_element(By.CLASS_NAME, "event__score--home").text.strip()
            away_score = el.find_element(By.CLASS_NAME, "event__score--away").text.strip()

            # como nao retorna o ano da partida, preciso fazer uma logica para considerar se a partida foi noano atual ou anterior, isso por causa dos jogos europeus, mas na proxima temporada nao é necessario essa logica, é só retornar o ano atual.
            dia_mes = date_time_raw.split()[0].rstrip('.')
            mes = int(dia_mes.split('.')[1])         
            ano_atual = datetime.now().year
            mes_atual = datetime.now().month  
            if mes > mes_atual:  
                ano = ano_atual -1  
            else:  
                ano = ano_atual  
            data_completa = f"{dia_mes}.{ano}"  
            data_final = datetime.strptime(data_completa, "%d.%m.%Y").strftime("%d/%m/%Y")

            data.append({
                "Campeonato": campeonato,
                "Temporada": season,
                "Rodada": current_round,
                "Data": data_final,
                "Hora": date_time_raw.split()[1],
                "Time da Casa": home_team,
                "Time Visitante": away_team,
                "Placar da Casa": home_score,
                "Placar do Visitante": away_score,
                "id": f"{home_team}_vs_{away_team}_{data_final}".replace(" ","")
            })

        except Exception as e:
            print(f"Erro ao extrair dados da partida: {e}")


for registro in data:
    for chave, valor in registro.items():
        print(f"{chave}: {valor}")
    print(f"\n---\n")
# for chave, valor in data.items():
#     print(f"{chave}: {valor}")

# try:
#     with open(f'data/raw/results/{campeonato}_season_{season.replace("/", "_")}.json', "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
#     print(f'Dados salvo em: src/data/raw/results/{campeonato}_season_{season.replace("/", "_")}.json')
# except Exception as e:
#     print("Erro ao salvar:", e)

driver.quit()
