# -*- coding: utf-8 -*-
"""
Created on Mon May 25 12:58:15 2020

@author: felip
"""

from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import pandas as pd
import numpy as np

from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt 

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk 
nltk.download('stopwords')
nltk.download('punkt')


#Setting a list with stopwords
stopwords= set(STOPWORDS)

#webpage 
bp_transcripts = 'https://www.cnnbrasil.com.br/politica/2020/05/22/leia-a-integra-da-transcricao-da-reuniao-ministerial-com-bolsonaro'

#Getting the content from the webpage
def get_soup(html):
    
    resp = requests.get(html)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, from_encoding=encoding)
    return soup

#filtering to pull back only the related text
def get_text(soup):
    all_text = [] 
    for i in soup.find_all('p'):
            all_text.append(i.get_text())
    return all_text 

#Filtering to Bolsonaro's Talks
def filter_bolsonaro(alltxt):
    right_texts = []
    for i in alltxt:
        if i.startswith("Jair Bolsonaro:") == True:
            right_texts.append(i) 
    return right_texts

def punctuation_stop(text):
    """remove punctuation and stop words"""
    filtered = []
    stop_words = set(nltk.corpus.stopwords.words('portuguese'))
    word_tokens = word_tokenize(text)
    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            filtered.append(w.lower())
    return filtered
    

soup = get_soup(bp_transcripts)

alltxt = get_text(soup)

alltxt = filter_bolsonaro(alltxt)

text = "".join(alltxt)
    
text = punctuation_stop(text)

new_words = []
with open("brazilianwords.txt", 'r', encoding = 'utf-8') as f:
    [new_words.append(word) for line in f for word in line.split()]

new_stopwords = stopwords.union(new_words)

text = ' '.join(text)


wc= WordCloud(background_color="white", width=1600, height=800, max_words=100, max_font_size=200,min_font_size=1, stopwords=new_stopwords)
wc.generate(text)

plt.figure(figsize=[20,20])
plt.imshow(wc)
plt.axis('off')
plt.show()