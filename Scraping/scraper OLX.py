import requests
from bs4 import BeautifulSoup
import pandas as pd

rezultate = []
links = []
# Scraper pentru preturile anunturilor de pe OLX
html_text = requests.get('https://www.olx.ro/imobiliare/').text
soup = BeautifulSoup(html_text, 'lxml')
anunturi_olx = soup.find_all('a', class_='css-1tqlkj0')
for a in anunturi_olx:
    href = a.get("href")
    links.append("https://www.olx.ro" + href)

for link in links:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    
    judete = soup.find_all('p', class_='css-z0m36u')
    judet = judete[1].get_text(strip=True) if len(judete) > 1 else None
        
    pret = soup.find('h3', class_='css-1m6jpd2').text.strip()
    print(judet)
 