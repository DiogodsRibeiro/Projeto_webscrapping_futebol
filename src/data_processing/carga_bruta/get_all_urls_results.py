import json
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

OUTPUT = "data/raw/all_urls/"
PATH = f'{OUTPUT}all_urls_results.json'
INPUT = "data/json/all_url.json"

def coletar_urls_estatisticas():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls_template = data["urls"]
    endpoint = "resultados"
    urls_input = [url.replace("{endpoint}", endpoint) for url in urls_template]

    driver = webdriver.Chrome()
    all_stats_links = []

    hoje = datetime.now().date()
    inicio_intervalo = hoje - timedelta(days=4)

    for URL in urls_input:
        if not URL.startswith("http"):
            print(f"URL inválida ignorada: {URL}")
            continue

        print(f"🌐 Acessando: {URL}")
        driver.get(URL)
        time.sleep(3)

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "event--results"))
            )
        except:
            print("Página não carregou corretamente, pulando.")
            continue
        
        try:
            leagues = driver.find_element(By.CLASS_NAME, "container__fsbody") \
                            .find_element(By.ID, "live-table") \
                            .find_element(By.CLASS_NAME, "event--results") \
                            .find_element(By.CLASS_NAME, "sportName.soccer") 

            elements = leagues.find_elements(By.CSS_SELECTOR, ".event__round, .event__match")

            for match in elements:
                try:
                    class_list = match.get_attribute("class")
                    if "event__match" not in class_list:
                        continue
                    
                    date_time_raw = match.find_element(By.CLASS_NAME, "event__time").text.strip()
                    dia_mes = date_time_raw.split()[0].rstrip('.')
                    dia = int(dia_mes.split('.')[0])
                    mes = int(dia_mes.split('.')[1])
                    ano = datetime.now().year
                    data_partida = datetime(ano, mes, dia).date()

                    if not (inicio_intervalo <= data_partida <= hoje):
                        continue

                    link = match.find_element(By.CSS_SELECTOR, "a.eventRowLink").get_attribute("href")
                    #all_stats_links.append(link + "/estatisticas-de-jogo")
                    #all_stats_links.append(link.rstrip("/") + "/resumo/estatisticas/0/")

                    if "/resumo/" in link and "?mid=" in link:
                        # substitui só a primeira ocorrência de "/resumo/"
                        new_link = link.replace("/resumo/", "/resumo/estatisticas/0/", 1)
                    else:
                        # fallback, caso venha em outro formato
                        new_link = link.rstrip("/") + "/resumo/estatisticas/0/"

                    all_stats_links.append(new_link)

                except Exception as e:
                    pass
        except Exception as e:
            print(f"Erro ao processar {URL}: {e}")
            continue

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(all_stats_links, f, ensure_ascii=False, indent=4)

    print(f"\n✅ {len(all_stats_links)} links (últimos 3 dias incluindo hoje) salvos em: {PATH}")
    driver.quit()

