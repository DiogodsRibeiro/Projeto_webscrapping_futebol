import json
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
                    link = match.find_element(By.CSS_SELECTOR, "a.eventRowLink").get_attribute("href")
                    all_stats_links.append(link + "/estatisticas-de-jogo")
                except:
                    pass
        except Exception as e:
            print(f"Erro ao processar {URL}: {e}")
            continue

    # Salva o resultado
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(all_stats_links, f, ensure_ascii=False, indent=4)

    print(f"\n✅ {len(all_stats_links)} links salvos em: {PATH}")
    driver.quit()