import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" 

r = requests.get(url)

soup = BeautifulSoup(r.content, "lxml")

names = soup.find_all('a', class_ = 'external text')
txt = []
for i in names:
    txt.append(i.text)
    
sp_lst = txt[:500]
print(sp_lst)
    