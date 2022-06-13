import requests
from bs4 import BeautifulSoup
import string
from googletrans import Translator

url = "https://claudia.abril.com.br/"
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')	

full_words = []
a = {}

to_links = soup.find_all('div', class_='col-s-12 col-l-4')
links = []
for i in to_links:
    try:
        sub_url = i.find('a', href=True)['href']
        sub_req = requests.get(sub_url)
        sub_soup = BeautifulSoup(sub_req.text, 'html.parser')	
        
        for j in sub_soup.find_all('p'):
            words = j.text
            words = words.translate(str.maketrans('', '', string.punctuation))
            words = words.translate(str.maketrans('', '', '\u0022'))
            words = words.lower()
            for k in words.split():
                full_words.append(k)
           # words = words.split(' ')
            #print(words)
    except:
        continue

for i in full_words:
    if i in a.keys():
        a[i] += 1
    else:
        a.update({i: 1})
a = dict(sorted(a.items(), key = lambda x: x[1], reverse=True))

eng = Translator()
for i in a:
    print(i, eng.translate(i, src='pt').text)
    if a[i] <= 2:
        break





