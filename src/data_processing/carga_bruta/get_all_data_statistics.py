import json
import time
from selenium import webdriver
import re
from datetime import datetime
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT = "data/raw/statistics/"
PATH = f'{OUTPUT}all_games_statistics.json'
INPUT_URL = "data/raw/all_urls/all_urls_results.json"

def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado

def esperar_elemento(driver, by, value, espera=10):
    return WebDriverWait(driver, espera).until(EC.presence_of_element_located((by, value)))

def esperar_todos_elementos(driver, classes, espera=15):
    for class_name in classes:
        WebDriverWait(driver, espera).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

def coletar_estatisticas_partidas():
    with open(INPUT_URL, "r", encoding="utf-8") as f:
        urls = json.load(f)

    todos_os_jogos = []
    driver = webdriver.Chrome()

    for url in urls:
        while True:
            try:
                driver.get(url)
                esperar_todos_elementos(driver, [
                    "wcl-row_OFViZ",
                    "wcl-awayValue_rQvxs",
                    "wcl-category_7qsgP",
                    "wcl-homeValue_-iJBW"
                ], espera=15)

                date = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text.strip().split(" ")[0]
                data_formatada = datetime.strptime(date, "%d.%m.%Y").strftime("%d/%m/%Y")

                home_team = driver.find_elements(By.CLASS_NAME, "duelParticipant__home")[0].text.strip()
                away_team = driver.find_elements(By.CLASS_NAME, "duelParticipant__away")[0].text.strip()

                id_value = f"{limpar_nome_arquivo(home_team)}_vs_{limpar_nome_arquivo(away_team)}_{data_formatada}".replace(" ", "")

                statistics = driver.find_element(By.CLASS_NAME, "container__livetable") \
                                   .find_elements(By.CLASS_NAME, "section")

                if not statistics:
                    raise Exception("Nenhuma estatística encontrada.")

                estatisticas = {}
                for section in statistics:
                    linhas = section.find_elements(By.CLASS_NAME, "wcl-row_OFViZ")
                    for linha in linhas:
                        try:
                            home_value_el = esperar_elemento(linha, By.CLASS_NAME, "wcl-homeValue_-iJBW")
                            category_el = esperar_elemento(linha, By.CLASS_NAME, "wcl-category_7qsgP")
                            away_value_el = esperar_elemento(linha, By.CLASS_NAME, "wcl-awayValue_rQvxs")

                            home_value = home_value_el.text.strip()
                            category = category_el.text.strip()
                            away_value = away_value_el.text.strip()

                            estatisticas[category] = {
                                "home_team": home_value,
                                "away_team": away_value
                            }
                        except Exception as e:
                            print(f"Erro ao coletar linha de estatística em {id_value}: {e}")

                game_stats = {
                    "date": data_formatada,
                    "id": id_value,
                    **estatisticas
                }

                todos_os_jogos.append(game_stats)
                print(f"✅ Coletado: {id_value}")

                if len(todos_os_jogos) % 100 == 0:
                    with open(PATH, "w", encoding="utf-8") as f:
                        json.dump(todos_os_jogos, f, ensure_ascii=False, indent=4)
                    print(f"💾 Progresso salvo com {len(todos_os_jogos)} jogos.")

                break  # sucesso: sai do while

            except Exception as e:
                print(f"❌ Erro ao processar {url}: {e}")
                try:
                    driver.quit()
                except:
                    pass
                print("🔄 Reiniciando navegador em 10 segundos...")
                time.sleep(10)
                driver = webdriver.Chrome()  # reabre navegador

        time.sleep(3)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(todos_os_jogos, f, ensure_ascii=False, indent=4)

    print(f"✅ {len(todos_os_jogos)} jogos salvos em: {PATH}")
    driver.quit()
