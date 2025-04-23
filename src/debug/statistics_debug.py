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

#sectionHeader sectionHeader--center stat__header section__title 
# sectionHeader sectionHeader--center stat__header section__title 

OUTPUT = "data/raw/statistics/"

URL = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"
URL2 = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"
URL3 = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"

driver = webdriver.Chrome()
driver.get(URL)
containers = driver.find_element(By.CLASS_NAME, "container__livetable") \
                  .find_element(By.CLASS_NAME, "section") 


for container in containers:
    home_value = container.find_element(By.CLASS_NAME, "wcl-homeValue_-iJBW").text.strip()
    category = container.find_element(By.CLASS_NAME, "wcl-category_7qsgP").text.strip()
    away_value = container.find_element(By.CLASS_NAME, "wcl-awayValue_rQvxs").text.strip()
    
    print(f"Home: {home_value} | Categoria: {category} | Away: {away_value}")

home_value = containers.find_element(By.CLASS_NAME, "wcl-homeValue_-iJBW").text.strip()
category = containers.find_element(By.CLASS_NAME, "wcl-category_7qsgP").text.strip()
away_value = containers.find_element(By.CLASS_NAME, "wcl-awayValue_rQvxs").text.strip()

print(f"Time da casa: {home_value} | Gols esperados (xG): {category} | Time visitante: {away_value}")