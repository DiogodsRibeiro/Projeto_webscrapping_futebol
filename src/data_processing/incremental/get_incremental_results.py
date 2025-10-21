import json
import os
import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, TimeoutException

OUTPUT = "data/staging/results/"

DIAS_RETROATIVOS = 4

def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado


def extrair_dados(url_resultado, ano_atual, carregar_todos=False):
    dados = []
    campeonato = ""
    season = "" 
    nacionalidade = ""
    driver = webdriver.Chrome()
    
    try:
        driver.get(url_resultado)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "event--results")))
        time.sleep(10)
        
        # Carregar todos os resultados se o parâmetro estiver ativado
        if carregar_todos:
            print("🔄 Carregando todos os resultados...")
            while True:
                try:
                    mostrar_mais = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="wcl-buttonLink"]'))
                    )
                    driver.execute_script("arguments[0].click();", mostrar_mais)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            '[data-testid="wcl-scores-match"], [data-testid="wcl-scores-result-row"], .event__match'
                        ))
                    )
                    time.sleep(1.5)
                except (TimeoutException, NoSuchElementException):
                    print("✅ Todos os resultados carregados ou botão sumiu.")
                    break
        try:
            jogo_nao_encontrado = driver.find_elements(By.CSS_SELECTOR, '[data-testid="wcl-scores-simpleText-02"]')
            
            if jogo_nao_encontrado:
                for elemento in jogo_nao_encontrado:
                    if "Jogo não encontrado" in elemento.text:
                        print(f"⚠️  Jogo não encontrado para a URL: {url_resultado}")
                        return [], "", "", ""
                        
        except Exception as e:
            print(f"Erro ao verificar 'Jogo não encontrado': {e}")
        
        # Extrair informações básicas da página
        try:
            season = driver.find_element(By.CLASS_NAME, "heading__info").text.strip()
            heading = driver.find_element(By.CLASS_NAME, "heading__title") 
            campeonato = heading.find_element(By.CLASS_NAME, "heading__name").text.strip() 
            nacionalidade = driver.find_elements(By.CLASS_NAME, "breadcrumb__link")[1].text.strip()
        except Exception as e:
            print(f"Erro ao extrair informações básicas: {e}")
            return [], "", "", ""

        try:
            leagues = driver.find_element(By.CLASS_NAME, "container__fsbody").find_element(By.ID, "live-table") \
                            .find_element(By.CLASS_NAME, "event--results") \
                            .find_element(By.CLASS_NAME, "sportName.soccer") 

            elements = leagues.find_elements(By.CSS_SELECTOR, ".event__round, .event__match")

            current_round = None
            hoje = datetime.now().date()
            inicio_intervalo = hoje - timedelta(days=DIAS_RETROATIVOS)

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
                        
                        # Lógica de ano para resultados (inversa do calendário)
                        if '/' not in season:
                            # Temporada simples (ex: "2025")
                            anos_na_temporada = re.findall(r'\d{4}', season)
                            ano = int(anos_na_temporada[0]) if anos_na_temporada else ano_atual
                        else:
                            # Temporada cruzada (ex: "2025/2026")
                            # Para resultados: se data > hoje, assume ano passado
                            data_hoje = datetime.now().date()
                            data_teste = datetime.strptime(f"{dia_mes}.{data_hoje.year}", "%d.%m.%Y").date()
                            ano = data_hoje.year - 1 if data_teste > data_hoje else data_hoje.year
                        
                        data_completa = f"{dia_mes}.{ano}"
                        data_datetime = datetime.strptime(data_completa, "%d.%m.%Y").date()

                        if not (inicio_intervalo <= data_datetime <= hoje):
                            continue

                        data_final = data_datetime.strftime("%d/%m/%Y")

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
            print(f"Erro ao processar elementos da página: {e}")

    except Exception as e:
        print(f"Erro ao processar a URL: {url_resultado}\n{e}")
    finally:
        driver.quit()

    return dados, campeonato, season, nacionalidade

with open("data/json/all_url.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    urls = [url.replace("{endpoint}", "resultados") for url in config["urls"]]

def carga_incremental_results(carregar_todos=False):
    ano_atual = datetime.now().year
    todos_os_dados = []

    print(f" Buscando jogos dos últimos {DIAS_RETROATIVOS} dias")

    for url_resultado in urls:
        print(f"\nProcessando: {url_resultado}")
        dados_partida, campeonato, season, nacionalidade = extrair_dados(url_resultado, ano_atual, carregar_todos)
        
        if not dados_partida and campeonato == "":
            print("➡️  Pulando para o próximo link...")
            continue
            
        print(f"{len(dados_partida)} jogos encontrados para {campeonato} ({nacionalidade})")
        todos_os_dados.extend(dados_partida)

    nome_arquivo = f'{OUTPUT}all_results_incremental.json'
    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, ensure_ascii=False, indent=4)

    print(f"\nTotal de {len(todos_os_dados)} jogos salvos em: {nome_arquivo}")

# Exemplos de uso:
#carga_incremental_results()                    # Extrai apenas últimos 7 dias
#carga_incremental_results(carregar_todos=True)  # Clica em "Mostrar mais" e extrai tudo