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
INPUT_URL = "data/raw/all_urls/all_urls_results.json"

def limpar_nome_arquivo(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome_formatado = re.sub(r'[^a-zA-Z0-9\s_-]', '', nome_sem_acentos)
    nome_formatado = re.sub(r'\s+', ' ', nome_formatado).strip()
    nome_formatado = nome_formatado.replace(' ', '_')
    return nome_formatado

def esperar_todos_elementos(driver, classes, espera=15):
    for class_name in classes:
        WebDriverWait(driver, espera).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

def coletar_estatisticas_partidas_incremental():
    with open(INPUT_URL, "r", encoding="utf-8") as f:
        urls = json.load(f)

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
    urls_com_falha = []  # Lista para armazenar URLs que falharam
    driver = webdriver.Chrome(options=options)

    for i, url in enumerate(urls):
        max_tentativas = 3
        tentativas = 0
        sucesso = False
        
        print(f"🔄 Processando URL {i+1}/{len(urls)}: {url}")
        
        while tentativas < max_tentativas and not sucesso:
            try:
                driver.get(url)
                
                # Espera todas as classes necessárias carregarem
                esperar_todos_elementos(driver, [
                    "wcl-row_2oCpS",
                    "wcl-awayValue_Y-QR1",
                    "wcl-category_6sT1J", 
                    "wcl-homeValue_3Q-7P",
                    "wcl-charts_UfKzp"
                ], espera=15)

                date = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text.strip().split(" ")[0]
                data_formatada = datetime.strptime(date, "%d.%m.%Y").strftime("%d/%m/%Y")

                home_team = driver.find_element(By.CLASS_NAME, "duelParticipant__home").find_element(By.CSS_SELECTOR, ".participant__participantName a").text.strip()
                away_team = driver.find_element(By.CLASS_NAME, "duelParticipant__away").find_element(By.CSS_SELECTOR, ".participant__participantName a").text.strip()

                id_value = f"{limpar_nome_arquivo(home_team)}_vs_{limpar_nome_arquivo(away_team)}_{data_formatada}".replace(" ", "")

                estatisticas = {}
                
                # Busca por linhas de estatísticas
                row_selectors = ['.wcl-row_2oCpS', '.wcl-row_OFViZ']
                linhas = []
                
                for row_selector in row_selectors:
                    linhas = driver.find_elements(By.CSS_SELECTOR, row_selector)
                    if linhas:
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
                            estatisticas[category] = {
                                "home_team": home_value,
                                "away_team": away_value
                            }
                            
                    except Exception as e:
                        continue

                if not estatisticas:
                    raise Exception("Nenhuma estatística encontrada.")

                game_stats = {
                    "date": data_formatada,
                    "id": id_value,
                    **estatisticas
                }

                todos_os_jogos.append(game_stats)
                print(f"✅ Coletado: {id_value}")
                sucesso = True  # Marca como sucesso para sair do loop

                # Salva progresso a cada 100 jogos
                if len(todos_os_jogos) % 100 == 0:
                    with open(PATH, "w", encoding="utf-8") as f:
                        json.dump(todos_os_jogos, f, ensure_ascii=False, indent=4)
                    print(f"💾 Progresso salvo com {len(todos_os_jogos)} jogos.")

            except Exception as e:
                tentativas += 1
                print(f"❌ Erro ao processar {url} (tentativa {tentativas}/{max_tentativas}): {e}")
                
                if tentativas >= max_tentativas:
                    urls_com_falha.append({
                        "url": url,
                        "erro": str(e),
                        "posicao": i + 1
                    })
                    print(f"🚫 URL falhou após {max_tentativas} tentativas: {url}")
                    break  # Desiste desta URL e vai para a próxima
                    
                # Reinicia navegador para próxima tentativa
                try:
                    driver.quit()
                except:
                    pass
                print(f"🔄 Reiniciando navegador em 10 segundos... (tentativa {tentativas + 1}/{max_tentativas})")
                time.sleep(10)
                driver = webdriver.Chrome(options=options)

        # Pausa entre URLs (apenas se houve sucesso)
        if sucesso:
            time.sleep(3)

    # Salva resultado final
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(todos_os_jogos, f, ensure_ascii=False, indent=4)

    # Salva URLs que falharam
    if urls_com_falha:
        falhas_path = f'{OUTPUT}urls_com_falha.json'
        with open(falhas_path, "w", encoding="utf-8") as f:
            json.dump(urls_com_falha, f, ensure_ascii=False, indent=4)
        print(f"⚠️  {len(urls_com_falha)} URLs falharam e foram salvas em: {falhas_path}")

    print(f"✅ {len(todos_os_jogos)} jogos coletados com sucesso!")
    print(f"❌ {len(urls_com_falha)} URLs falharam")
    print(f"📁 Dados salvos em: {PATH}")
    
    driver.quit()

# if __name__ == "__main__":
#     coletar_estatisticas_partidas_incremental()