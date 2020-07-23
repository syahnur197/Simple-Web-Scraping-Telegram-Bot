from bs4 import BeautifulSoup

import requests

response = requests.get('https://www.bizbrunei.com/')

html = response.text

soup = BeautifulSoup(html, "html.parser")

titles = soup.find_all(class_='entry-title')

for title in titles:
    anchor = title.find('a')
    print(anchor.text)
    print("\n")

