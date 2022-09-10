import requests
from bs4 import BeautifulSoup
import string
from googletrans import Translator
import csv
import time

print(time.time(), 'start')
# pull html from main website
url = "https://claudia.abril.com.br/"
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
print(time.time(), 'main page')

words_to_clean = ''
freq_of_words = {}

# grab the links from the top articles on the website
to_links = soup.find_all('div', class_='col-s-12 col-l-4')
for i in to_links:
    try:
        sub_url = i.find('a', href=True)['href']
        sub_req = requests.get(sub_url)
        sub_soup = BeautifulSoup(sub_req.text, 'html.parser')
        # print(time.time(), 'sub link retrieved')

        for j in sub_soup.find_all('p'):
            words_to_clean = words_to_clean + j.text + ' '
            # print(time.time(), 'text written')
    except:
        continue
print(time.time(), 'grabbed text')

# clean up string
words_to_clean = words_to_clean.lower()
cleaned_words = ''
for i in words_to_clean:
    if (i.isalnum() or i == ' '):
        cleaned_words = cleaned_words + i
print(time.time(), 'cleaned up text')

# put words into dictionary
for i in cleaned_words.split(' '):
    if i in freq_of_words.keys():
        freq_of_words[i]+=1
    else:
        freq_of_words.update({i:1})
print(time.time(), 'dictionary filled')

# sort string from most frequent to least frequent
freq_of_words = dict(sorted(freq_of_words.items(), key = lambda x: x[1], reverse=True))
print(time.time(), 'dictionary sorted')

# write to csv
eng = Translator()
with open('top_words.csv', 'w') as csvfile:
    csvfile.flush()
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Portuguese', 'English', 'Frequency'])
    print(time.time(), 'head row written')
    rows_written = 0 # only used for print(time.time(),...) statements
    for i in freq_of_words.keys():
        try:
            csvwriter.writerow([i, eng.translate(i, src='pt').text, freq_of_words[i]])
            rows_written+=1
            if rows_written % 20 == 0:
                print(time.time(), rows_written, 'rows written')
            # if rows_written > 50:
            #     csvfile.close()
            #     break
        except:
            print(time.time(), 'could not write', i)
            continue
    csvfile.close()





#
