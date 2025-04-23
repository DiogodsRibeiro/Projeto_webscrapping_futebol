from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.flashscore.com.br/jogo/futebol/UqMsyH9c/#/resumo-de-jogo/estatisticas-de-jogo/2"

driver = webdriver.Chrome()
driver.get(URL)

# Esperar carregar o elemento com a data/hora
data_hora = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "duelParticipant__startTime"))
)

print("Data e hora do jogo:", data_hora.text)

driver.quit()