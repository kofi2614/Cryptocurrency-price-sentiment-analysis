from __future__ import division
import pickle

import requests
import pprint as pp
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
import csv
import bs4
import sqlite3
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import urllib
from urllib import request
#urllib.request(url)
import datetime
from datetime import timedelta
import urllib3
from urllib3 import util
from dateutil import parser
import random as rand

f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

#get today's
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0')]
t= (datetime.date.today()- datetime.date(2018,1,1)).days
t=str(t)
url18='https://www.google.ca/search?q=bitcoin&client=ubuntu&hs=rzn&channel=fs&dcr=0&biw=1295&bih=565&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F'+t+'%2F2018%2Ccd_max%3A1%2F'+t+'%2F2018&tbm=nws'
html = opener.open(url18)
soup = bs4.BeautifulSoup(html.read(), "html.parser")
#print(soup.prettify())
letters = soup.find_all("div", class_="st")

lettersClean=[]

string = str(letters[0])
toRemove = ['<div class="st">', '</div>', '<b>Bitcoin</b>', '<em>Bitcoin</em>', 'xa0', '\\']
for element in toRemove:
    string = string.replace(element, "")
lettersClean.append(string)

stop_words = set(stopwords.words('english') + ['cryptocurrency', 'cryptocurrencies', 'u', '000', 'em', 'bitcoin', 'ha', 'wa', 'de','en','la','el'])
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+') # takes only alphanum characters

word_tokens = tokenizer.tokenize(lettersClean[0])
word_lower = [w.lower() for w in word_tokens]
word_stem = [lemmatizer.lemmatize(w) for w in word_lower]
filtered_row = [w for w in word_stem if not w in stop_words]

topKey=['price', 'currency', 'exchange', 'digital', 'market', 'new', 'time', 'year', 'blockchain', 'one', 'trading', 'high', '1', 'bank', 'week', 'company', 'value', 'said', 'transaction', 'world', 'investor', 'user', 'first', 'day', 'would', 'according', 'last', 'ethereum', 'like', 'money', 'people', 'technology', 'financial', 'month', 'since', 'future', 'percent', 'fund', 'coin', 'investment', 'payment', 'based', 'two', 'could', 'many', 'also', 'around', '2', 'bitcoins', 'may', 'past', 'mining', 'asset', 'network', 'cash', 'service', 'china', 'gold', 'country', '2017', 'government', 'recent', 'today', 'record', 'platform', 'even', 'come', 'btc', 'use', 'wallet', 'virtual', 'still', 'dollar', 'however', '4', 'data', 'business', 'news', 'announced', 'way', 'recently', 'make', 'global', 'central', 'block', 'fork', 'miner', 'report', 'called', 'say', 'largest', 'support', 'group', 'well', 'gain', '10', 'back', 'security', 'trade', 'move', '5', '3', 'rise', 'million', 'hit', 'much', 'worth', 'another', 'per', 'long', 'coindesk', 'firm', 'com', 'trader', 'major', 'mark', 'see', 'made', 'used', 'system', 'traded', 'industry', 'hard', 'state', 'crypto', 'number', 'coinbase', 'hour', 'using', 'known', 'take', 'bubble', 'three', 'ceo', 'seen', 'buy', 'friday', 'account', 'lot', 'etf', 'chinese', 'become', 'developer', 'billion', 'level', 'including', 'earlier', 'development', '6', 'computer', 'early', 'increase', 'fee', 'popular', 'set', 'volume', 'plan', '500', 'tuesday', 'part', 'online', 'term', 'le', 'nearly', 'though', 'token', 'big', 'top', 'litecoin', 'usd', 'press', 'get', 'japan', 'end', 'statement', 'next', 'startup', 'low', 'currently', 'customer', 'quite', 'demand', 'community', 'segwit', 'founder', 'india', 'thing', 'look', '20', 'software', 'capital', 'think', 'following', 'potential', 'several', 'far', 'within', 'reported', '100', 'risk', 'ago']

dictionary = {}
for word in filtered_row:
    if word in topKey:
        dictionary[word] = True
    else:
        dictionary[word] = False

#x=classifier.prob_classify(dictionary)

if classifier.classify(dictionary)==1:
    title='Bitcoin price expected to increase today!'
else:
    title='Bitcoin price expected to decrease today!'

titleL=[[title]]

conn = sqlite3.connect('crypto.db')  # connection
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS sentiment')
c.execute('CREATE TABLE sentiment (title TEXT)')
c.executemany('INSERT INTO sentiment VALUES(?)', titleL)
conn.commit()
conn.close()
'''
def tableFromDatabase(database, table):
    conn = sqlite3.connect(database)  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT * FROM %s' % table)
    tableRows = c.fetchall()
    return tableRows

conn.close()
title = tableFromDatabase('crypto.db', 'sentiment')
'''
