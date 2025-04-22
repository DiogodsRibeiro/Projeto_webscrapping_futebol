import json
import os
import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import random

# Configurações
PASTA_SAIDA = "data/raw/statistics/"
URL = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"

# Iniciar o navegador
driver = webdriver.Chrome()
driver.get(URL)

# Esperar o carregamento da página
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "container__livetable"))
    )
    
    # Tentar encontrar o elemento com a data/hora
    cabecalho = driver.find_element(By.CLASS_NAME, "sectionHeader--center")
    data_hora = cabecalho.text.strip()
    print(f"Data e hora encontradas: {data_hora}")
    
    # Aqui você pode processar/salvar os dados como quiser
    # Exemplo: extrair apenas a data
    # data = data_hora.split()[0]  # assumindo que a data vem primeiro
    
except NoSuchElementException as e:
    print(f"Erro: Elemento não encontrado - {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    # Fechar o navegador mesmo se ocorrer erro
    driver.quit()