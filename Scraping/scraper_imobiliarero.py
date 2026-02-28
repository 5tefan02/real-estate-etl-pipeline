from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

def scrape_imobiliarero():
    rezultate = []
    links = []

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get('https://www.imobiliare.ro/vanzare-imobiliare')
    time.sleep(5) 

    soup = BeautifulSoup(driver.page_source, 'lxml')
    anunturi_imobiliare = soup.find_all('a', {'data-cy': 'listing-information-link'})
    
    for a in anunturi_imobiliare:
        href = a.get("href")
        links.append("https://www.imobiliare.ro" + href)
    links = list(set(links))

    for link in links:
        try:
            driver.get(link)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            oras_raw = soup.find('span', {'data-cy': 'location-text'})
            oras = oras_raw.text.strip() if oras_raw else ""
        except Exception as e:
            print(f"Eroare la link-ul {link}: {e}")
            continue
        
    driver.quit()
    return rezultate
