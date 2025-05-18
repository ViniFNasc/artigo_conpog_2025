from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json


class Connection:

    def __init__(self):

        pass
 

    def get_events(self,data):

        url = f'https://www.sofascore.com/api/v1/sport/football/scheduled-events/{data}'
        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(0.5)

        texto_completo = driver.find_element(By.TAG_NAME, "body").text

        driver.close()

        obj = json.loads(texto_completo)
        events = obj['events']
        time.sleep(0.5)

        return events


    def get_statistics(self, match_id):

        url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(0.5)

        texto_completo = driver.find_element(By.TAG_NAME, "body").text

        driver.close()

        obj = json.loads(texto_completo)
        statistics = obj['statistics']
        time.sleep(0.5)

        return statistics




    def get_markets(self,match_id):

        url = f'https://www.sofascore.com/api/v1/event/{match_id}/odds/1/all'

        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(0.5)

        texto_completo = driver.find_element(By.TAG_NAME, "body").text

        driver.close()

        obj = json.loads(texto_completo)
        markets = obj['markets']
        time.sleep(0.5)

        return markets





    def get_season(self,match_id):

        url = f"https://www.sofascore.com/api/v1/event/{match_id}"

        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(0.5)

        texto_completo = driver.find_element(By.TAG_NAME, "body").text

        driver.close()

        obj = json.loads(texto_completo)
        event = obj['event']
        time.sleep(0.5)

        return event