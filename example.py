from bs4 import BeautifulSoup

import requests

response = requests.get('https://mediapermata.com.bn/')

html = response.text

soup = BeautifulSoup(html, "html.parser")

titles = soup.find_all(class_='entry-title')

for title in titles:
    print(title.text)
    print("\n")

