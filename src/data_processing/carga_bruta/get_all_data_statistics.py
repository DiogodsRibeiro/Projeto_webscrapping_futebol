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

OUTPUT = "data/raw/statistics/"

URL = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"

driver = webdriver.Chrome()
driver.get(URL)
containers = driver.find_element(By.CLASS_NAME, "container__livetable") \
                  .find_elements(By.CLASS_NAME, "section") \

dados = {}

for section in containers:
    elementos = section.find_elements(By.CLASS_NAME, "wcl-row_OFViZ")


    for elemento in elementos:

        home_value = elemento.find_element(By.CLASS_NAME, "wcl-homeValue_-iJBW").text.strip()
        category = elemento.find_element(By.CLASS_NAME, "wcl-category_7qsgP").text.strip()
        away_value = elemento.find_element(By.CLASS_NAME, "wcl-awayValue_rQvxs").text.strip()



        if category not in dados:
            dados[category] = {
                "time_casa": home_value,
                "time_visitante": away_value
            }




print(dados)

driver.quit()

