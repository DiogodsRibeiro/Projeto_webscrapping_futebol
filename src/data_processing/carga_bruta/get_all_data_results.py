from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from  datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import os
import re
import unicodedata

def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado

with open("data/json/urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)["urls"]

arquivos_salvos = []

for url_resultado in urls:
    print(f"\nProcessando: {url_resultado}")
    driver = webdriver.Chrome()
    driver.get(url_resultado)

    ano_atual = datetime.now().year

    try:
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
        campeonato = driver.find_element(By.CLASS_NAME, "heading__title") \
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

                    dia_mes = date_time_raw.split()[0].rstrip('.')
                    mes = int(dia_mes.split('.')[1])
                    mes_atual = datetime.now().month

                    ano = ano_atual - 1 if mes > mes_atual else ano_atual
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
                        "id": f"{home_team}_vs_{away_team}_{data_final}".replace(" ", "")
                    })

                except Exception as e:
                    print(f"Erro ao extrair dados da partida: {e}")


        nome_liga_formatado = limpar_nome_arquivo(campeonato)

        try:
            nome_arquivo = f'data/raw/results/{nome_liga_formatado}_season_{season.replace("/", "_")}.json'
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            arquivos_salvos.append(nome_arquivo)
            print(f'Dados salvos em: {nome_arquivo}')
        except Exception as e:
            print("Erro ao salvar:", e)

    except Exception as e:
        print(f"Erro ao processar a URL: {url_resultado}\n{e}")

    driver.quit()

print(f'\nLoop encerrado para todas as URLs. Arquivos criados:')
for arquivo in arquivos_salvos:
    print(f" - {arquivo}")