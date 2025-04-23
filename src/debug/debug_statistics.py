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

# sectionHeader sectionHeader--center stat__header section__title 

OUTPUT = "data/raw/statistics/"

URL = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"

driver = webdriver.Chrome()
driver.get(URL)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "container__livetable")))

tabela_Principais = driver.find_element(By.CLASS_NAME, "container__livetable") \
                .find_element(By.CLASS_NAME, "section") 
                


print(tabela_Principais.text)
