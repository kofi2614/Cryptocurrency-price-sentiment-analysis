from __future__ import division
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
from collections import Counter
import math
from xml.etree import ElementTree
import urllib
from urllib import request
#urllib.request(url)
import datetime
from datetime import timedelta
import urllib3
from urllib3 import util
from dateutil import parser
import random as rand


#bring in csv file
prices = []
with open('/home/datascience//Desktop/Project_A/crypto-markets.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        prices.append(row)
titles=prices[0]
prices=prices[1:]

close=[]
priceDates=[]


letters17=[]
with open('/home/datascience//Desktop/Project_A/letters.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        letters17.append(row)
dates17=[]
with open('/home/datascience//Desktop/Project_A/dates.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        dates17.append(row)

dates17= [parser.parse(row[0]) for row in dates17]

for row in prices:
    if row[0]=='bitcoin':
        close.append(float(row[8]))
        d=row[3].split('-')
        priceDate = datetime.datetime(int(d[0]),int(d[1]),int(d[2]))
        priceDates.append(priceDate)

# [above 5% absolute change =1, positive change=1, both 1s=1, [1,0]=0]
percChanges=[]
target=[]
for i in range(0,len(close)-1):
    row = []
    percChange = (close[i] - close[i + 1]) / close[i]
    percChanges.append(percChange)
    if percChange > 0:
        positive=1
    else:
        positive = 0
    target.append(positive)

pricesTable=[]
for i in range(len(priceDates)):
    row=[]
    if i==0:
        row=[priceDates[i],0]
    else:
        row.append(priceDates[i])
        row.append(target[i-1])
    pricesTable.append(row)

lettersClean=[]
for row in letters17:
    string = str(row)
    toRemove = ['<div class="st">', '</div>', '<b>Bitcoin</b>', '<em>Bitcoin</em>', 'xa0', '\\']
    for element in toRemove:
        string = string.replace(element, "")
    lettersClean.append(string)

# normalize words
stop_words = set(stopwords.words('english') + ['cryptocurrency', 'cryptocurrencies', 'u', '000', 'em', 'bitcoin', 'ha', 'wa', 'de','en','la','el'])
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+') # takes only alphanum characters

normal = []
counts = []
for row in lettersClean:
    word_tokens = tokenizer.tokenize(row)
    word_lower = [w.lower() for w in word_tokens]
    word_stem = [lemmatizer.lemmatize(w) for w in word_lower]
    filtered_row = [w for w in word_stem if not w in stop_words]
    normal.append(filtered_row)
    counts.append(Counter(filtered_row))


allWords = []
for row in normal:
    for word in row:
        allWords.append(word)
countsWords = Counter(allWords)
#swtich term frequency to tfidf
sortWords = sorted(countsWords, key=countsWords.get, reverse=True)

# calculate tf-idf
def inverse_freq(all_documents):
    idf_values = {}
    all_tokens_set = set([item for row in all_documents for item in row])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, all_documents)
        idf_values[tkn] = math.log(len(all_documents) / (sum(contains_token)))
    return idf_values

#def tfidf(term, all_documents):
idf = inverse_freq(normal)
tfidfs = {}
for term in idf:
       tfidf = idf[term]*countsWords[term]
       tfidfs[term]=tfidf

#sortedTfidfs = sorted(tfidfs.items(), key=lambda x:x[1], reverse = True)
sortVal = sorted(tfidfs.values(), reverse=True)
sortKey = sorted(tfidfs, key=tfidfs.get, reverse=True)

topKey = sortKey[:201]

datesPlusNormal=[]
for i in range(len(counts)):
    row =[]
    row.append(dates17[i])
    row.append(normal[i])
    datesPlusNormal.append(row)

wordsPlusTarget=[]
for i in range(len((datesPlusNormal))):
    row=[]
    row.append(datesPlusNormal[i][1])
    for j in range(len(pricesTable)):
        if datesPlusNormal[i][0]==pricesTable[j][0]:
            row.append(pricesTable[j][1])
            #print('yes', j, row)
    wordsPlusTarget.append(row)

lilAllWords = allWords[:10]
#lilWordsTarget = wordsPlusTarget[:10]
topWords = sortWords[:5]

t=[]
for i in range(len(wordsPlusTarget)):
    row = []
    dictionary = {}
    for j in range(len(wordsPlusTarget[i][0])):
        if wordsPlusTarget[i][0][j] in topKey:
            dictionary[wordsPlusTarget[i][0][j]] = True
        else:
            dictionary[wordsPlusTarget[i][0][j]] = False
    row.append(dictionary)
    row.append(wordsPlusTarget[i][1])
    t.append(row)
'''
count1s=0
tBinary=[]
for row in t:
    if row[1] != 2:
        tBinary.append(row)
    if row[1]==1:
        count1s+=1
'''

balanced=[]
for row in t:
    if row[1]==0:
        balanced.append(row)
balanced=balanced[:1400]
for row in t:
    if row[1]==1:
        balanced.append(row)

rand.shuffle(balanced)

train = balanced[:2520]

test = balanced[2520:]

classifier = nltk.NaiveBayesClassifier.train(train)

#print(nltk.classify.accuracy(classifier, test))

#print(classifier.show_most_informative_features(20))

import pickle
f = open('my_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

'''

x=[]
y=[]
trace1 = go.Scatter(
    x=x,
    y=y,
)
data = [trace1]
layout = go.Layout(title=title, titlefont=dict(
            size=32),
    )
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='prediction')
'''