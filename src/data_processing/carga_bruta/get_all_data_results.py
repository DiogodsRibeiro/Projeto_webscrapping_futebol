import json
import os
import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

OUTPUT = "data/raw/results/"



def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado


def extrair_dados(url_resultado, ano_atual):
    dados = []
    driver = webdriver.Chrome()
    driver.get(url_resultado)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "event--results")))
        time.sleep(10)
        
        # while True:
        #     try:
        #         mostrar_mais = driver.find_element(By.CLASS_NAME, "event__more")
        #         driver.execute_script("arguments[0].click();", mostrar_mais)
        #         time.sleep(8)
        #     except NoSuchElementException:
        #         break

        season = driver.find_element(By.CLASS_NAME, "heading__info").text.strip()

        heading = driver.find_element(By.CLASS_NAME, "heading__title") 
        campeonato = heading.find_element(By.CLASS_NAME, "heading__name").text.strip() 
        nacionalidade = driver.find_elements(By.CLASS_NAME, "breadcrumb__link")[1].text.strip() 

        leagues = driver.find_element(By.CLASS_NAME, "container__fsbody").find_element(By.ID, "live-table") \
                        .find_element(By.CLASS_NAME, "event--results") \
                        .find_element(By.CLASS_NAME, "sportName.soccer") 

        elements = leagues.find_elements(By.CSS_SELECTOR, ".event__round, .event__match")

        current_round = None
        for el in elements:
            class_list = el.get_attribute("class")

            if "event__round" in class_list:
                current_round = el.text.strip()

            elif "event__match" in class_list:
                try:
                    date_time_raw = el.find_element(By.CLASS_NAME, "event__time").text.strip()
                    home_team = el.find_element(By.CLASS_NAME, "event__homeParticipant").text.strip().split("\n")[0]
                    away_team = el.find_element(By.CLASS_NAME, "event__awayParticipant").text.strip().split("\n")[0]
                    home_score = el.find_element(By.CLASS_NAME, "event__score--home").text.strip()
                    away_score = el.find_element(By.CLASS_NAME, "event__score--away").text.strip()

                    dia_mes = date_time_raw.split()[0].rstrip('.')
                    mes = int(dia_mes.split('.')[1])
                    ano = ano_atual - 1 if mes > datetime.now().month else ano_atual
                    data_completa = f"{dia_mes}.{ano}"
                    data_final = datetime.strptime(data_completa, "%d.%m.%Y").strftime("%d/%m/%Y")

                    dados.append({
                        "origem": nacionalidade.capitalize(),
                        "Campeonato": campeonato,
                        "Temporada": season,
                        "Rodada": current_round,
                        "Data": data_final,
                        "Hora": date_time_raw.split()[1],
                        "Time da Casa": home_team,
                        "Time Visitante": away_team,
                        "Placar da Casa": home_score,
                        "Placar do Visitante": away_score,
                        "id": f"{limpar_nome_arquivo(home_team)}_vs_{limpar_nome_arquivo(away_team)}_{data_final}".replace(" ", "")
                    })

                except Exception as e:
                    print(f"Erro ao extrair dados da partida: {e}")

    except Exception as e:
        print(f"Erro ao processar a URL: {url_resultado}\n{e}")
    finally:
        driver.quit()

    return dados, campeonato, season, nacionalidade

with open("data/json/all_url.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    urls = [url.replace("{endpoint}", "resultados") for url in config["urls"]]

def carga_bruta():
    ano_atual = datetime.now().year

    for url_resultado in urls:
        print(f"\nProcessando: {url_resultado}")
        dados_partida, campeonato, season, nacionalidade = extrair_dados(url_resultado, ano_atual)

        nome_liga_formatado = limpar_nome_arquivo(campeonato)
        nome_origem_formatado = limpar_nome_arquivo(nacionalidade)
        nome_arquivo = f'{OUTPUT}{nome_origem_formatado.lower()}_{nome_liga_formatado}_season_{season.replace("/", "_")}.json'

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_partida, f, ensure_ascii=False, indent=4)

        print(f"{len(dados_partida)} jogos salvos em: {nome_arquivo}")  