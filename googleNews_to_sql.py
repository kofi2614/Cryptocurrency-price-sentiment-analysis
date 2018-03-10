from __future__ import division
import requests
import pprint as pp
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
import csv
import bs4
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import pprint
import sqlite3
import plotly
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

url3= 'https://www.google.ca/search?q=bitcoin&client=ubuntu&channel=fs&dcr=0&biw=1295&bih=565&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2014%2Ccd_max%3A3%2F1%2F2014&tbm=nws'

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0')]

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
    row=[]
    percChange=(close[i]-close[i+1])/close[i]
    percChanges.append(percChange)
    if abs(percChange)>0.05:
        absChange = 1
    else:
        absChange = 0
    row.append(absChange)
    if percChange > 0:
        positive=1
    else:
        positive = 0
    row.append(positive)
    if absChange ==1 and positive ==1:
        bigAndPositve=1
    elif absChange ==1 and positive ==0:
        bigAndPositve = 0
    else:
        bigAndPositve = 2
    row.append(bigAndPositve)
    target.append(row)

pricesTable=[]
for i in range(len(priceDates)):
    row=[]
    if i==0:
        row=[priceDates[i],0]
    else:
        row.append(priceDates[i])
        row.append(target[i-1][2])
    pricesTable.append(row)

#web scraping portion - ran to populate csv files


#2017 data from web
date = datetime.date(2017,1,1)
dates17 = []
letters17=[]
for t in range(1,366):
    t = str(t)
    url17= 'https://www.google.ca/search?q=bitcoin&client=ubuntu&hs=FKM&channel=fs&dcr=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F'+t+'%2F2017%2Ccd_max%3A1%2F'+t+'%2F2017&tbm=nws'
    html = opener.open(url17)
    soup = bs4.BeautifulSoup(html.read(), "html.parser")
    #print(soup.prettify())
    letters = soup.find_all("div", class_="st")
    for row in letters:
        letters17.append(row)
        dates17.append(date)
    date = date+datetime.timedelta(days=1)

lettersClean=[]
for row in letters17:
    string = str(row)
    toRemove = ['<div class="st">', '</div>', '<b>Bitcoin</b>', '<em>Bitcoin</em>', 'xa0', '\\']
    for element in toRemove:
        string = string.replace(element, "")
    lettersClean.append(string)

# normalize words
stop_words = set(stopwords.words('english') + ['cryptocurrency', 'cryptocurrencies', 'u', '000'])
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



datesPlusCounts=[]
for i in range(len(counts)):
    row =[]
    row.append(dates17[i])
    row.append(counts[i])
    datesPlusCounts.append(row)

wordsPlusTarget=[]
for i in range(len((datesPlusCounts))):
    row=[]
    row.append(datesPlusCounts[i][1])
    for j in range(len(pricesTable)):
        if datesPlusCounts[i][0]==pricesTable[j][0]:
            row.append(pricesTable[j][1])
            #print('yes', j, row)
    wordsPlusTarget.append(row)

#above 5% change only
above5 = []
for row in wordsPlusTarget:
    if row[1] != 2:
        above5.append(row)

def get_word_features(wordlist):
	    wordlist = nltk.FreqDist(wordlist)
	    word_features = wordlist.keys()
	    return word_features

word_features = get_word_features(normal[0])

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
	return features
'''
t = [({word for word in allWords}, x[1] for x in wordsPlusTarget]



array = np.array(wordsPlusTarget)
target= array[:,1]

train = wordsPlusTarget[:3286]
trainBinary = above5[:3286]
test = wordsPlusTarget[3286:]
testBinary = above5[3286:]

classifier = nltk.NaiveBayesClassifier.train(trainBinary)

print(nltk.classify.accuracy(classifier, testBinary))

print(classifier.show_most_informative_features(20))
'''
#date = datetime.date(2017,1,1)
#dates17 = []
letters17=[]
for t in range(1,366):
    t = str(t)
    url17= 'https://www.google.ca/search?q=bitcoin&client=ubuntu&hs=FKM&channel=fs&dcr=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F'+t+'%2F2017%2Ccd_max%3A1%2F'+t+'%2F2017&tbm=nws'
    html = opener.open(url17)
    soup = bs4.BeautifulSoup(html.read(), "html.parser")
    #print(soup.prettify())
    letters = soup.find_all("div", class_="st")
    for row in letters:
        letters17.append(row)
        dates17.append(date)
    date = date+datetime.timedelta(days=1)

copyL =[letters17]
copyD = [dates17]

lettersBrackets= [[row] for row in lettersClean]
datesBrackets=[[row] for row in dates17]

with open('/home/datascience//Desktop/Project_A/letters.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(lettersBrackets)

with open('/home/datascience//Desktop/Project_A/dates.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(datesBrackets)