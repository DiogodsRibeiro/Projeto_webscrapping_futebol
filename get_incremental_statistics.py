import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT = "data/staging/statistics/"
PATH = f'{OUTPUT}incremental_games_statistics.json'

def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado

def coletar_estatisticas_partidas_incremental():
    # URL única para teste
    url = "https://www.flashscore.com.br/jogo/futebol/bk18CtYr/#/resumo-de-jogo/estatisticas-de-jogo/0"
    
    # Configurações para reduzir mensagens do Chrome
    options = Options()
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    options.add_argument('--disable-gpu-logging')
    options.add_argument('--disable-extensions-logging')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    todos_os_jogos = []
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        
        # Aguarda o carregamento das estatísticas
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.wcl-row_2oCpS, .container__livetable .section'))
        )

        # Extrai data do jogo
        date = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text.strip().split(" ")[0]
        data_formatada = datetime.strptime(date, "%d.%m.%Y").strftime("%d/%m/%Y")

        # Extrai nomes dos times
        home_team = driver.find_elements(By.CLASS_NAME, "duelParticipant__home")[0].text.strip()
        away_team = driver.find_elements(By.CLASS_NAME, "duelParticipant__away")[0].text.strip()

        id_value = f"{limpar_nome_arquivo(home_team)}_vs_{limpar_nome_arquivo(away_team)}_{data_formatada}".replace(" ", "")

        # Método alternativo: Usando classes wcl-row
        estatisticas = {}
        
        # Busca por linhas de estatísticas
        row_selectors = ['.wcl-row_2oCpS', '.wcl-row_OFViZ']
        linhas = []
        
        for row_selector in row_selectors:
            linhas = driver.find_elements(By.CSS_SELECTOR, row_selector)
            if linhas:
                print(f"Encontrou {len(linhas)} linhas com seletor: {row_selector}")
                break
        
        for linha in linhas:
            try:
                # Tenta diferentes combinações de classes para home/away/category
                home_selectors = [
                    '.wcl-homeValue_3Q-7P', '.wcl-homeValue_-iJBW', 
                    '[class*="homeValue"]'
                ]
                away_selectors = [
                    '.wcl-awayValue_Y-QR1', '.wcl-awayValue_rQvxs',
                    '[class*="awayValue"]'
                ]
                category_selectors = [
                    '.wcl-category_6sT1J', '.wcl-category_7qsgP',
                    '[class*="category"]'
                ]
                
                home_value, away_value, category = None, None, None
                
                # Busca home value
                for selector in home_selectors:
                    try:
                        home_value = linha.find_element(By.CSS_SELECTOR, selector).text.strip()
                        break
                    except:
                        continue
                
                # Busca away value  
                for selector in away_selectors:
                    try:
                        away_value = linha.find_element(By.CSS_SELECTOR, selector).text.strip()
                        break
                    except:
                        continue
                
                # Busca category
                for selector in category_selectors:
                    try:
                        category = linha.find_element(By.CSS_SELECTOR, selector).text.strip()
                        break
                    except:
                        continue

                if home_value and away_value and category:
                    print(f"Estatística encontrada: {category} | Casa: {home_value} | Fora: {away_value}")
                    estatisticas[category] = {
                        "home_team": home_value,
                        "away_team": away_value
                    }
                else:
                    print(f"Dados incompletos - Casa: {home_value}, Fora: {away_value}, Categoria: {category}")
                    
            except Exception as e:
                print(f"Erro ao processar linha: {e}")
                continue

        if not estatisticas:
            print("Nenhuma estatística foi extraída. Inspecionando HTML...")
            
            # Debug: mostra algumas classes encontradas na página
            all_divs = driver.find_elements(By.TAG_NAME, "div")[:50]  # primeiros 50 divs
            for div in all_divs:
                class_name = div.get_attribute("class")
                if class_name and ("wcl" in class_name or "statistic" in class_name):
                    print(f"Classe encontrada: {class_name}")

        game_stats = {
            "date": data_formatada,
            "id": id_value,
            "total_estatisticas": len(estatisticas),
            **estatisticas
        }

        todos_os_jogos.append(game_stats)
        print(f"Coletado: {id_value} ({len(estatisticas)} estatísticas)")

        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(todos_os_jogos, f, ensure_ascii=False, indent=4)

        print(f"{len(todos_os_jogos)} jogos salvos em: {PATH}")

    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
        
        # Debug adicional
        try:
            page_source = driver.page_source
            if "wcl-row" in page_source:
                print("Classes wcl-row* encontradas no HTML")
            if "statistics" in page_source.lower():
                print("Palavra 'statistics' encontrada no HTML")
        except:
            pass

    finally:
        driver.quit()

if __name__ == "__main__":
    coletar_estatisticas_partidas_incremental()