from __future__ import division
import pprint
import sqlite3
import requests
import numpy as np
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
import random as rand


coinsNewsURL = requests.get(
    "https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=1d656ac0916147bf8d28e1dcda71266a")

coinsNews = coinsNewsURL.json()  # this is a dictionary
# keys are: [u'status', u'articles', u'totalResults']

articles = coinsNews['articles']
dicKeys = articles[0].keys() # [u'description',u'title', u'url', u'author', u'publishedAt', u'source', u'urlToImage']
keys = []
for element in dicKeys:
    if element != 'source':
        keys.append(element)

articlesList = []
colId = 0
for i in range(0, len(articles)):
    article = []
    article.append(colId)
    for j in range(0, 6):
        article.append(articles[i][keys[j]])
    # print i, j, article
    articlesList.append(article)
    colId +=1


# feed from website to sql table
conn = sqlite3.connect('crypto.db')  # connection
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS coinsNews')
c.execute('CREATE TABLE coinsNews(id INTEGER, author TEXT, title TEXT, description TEXT, url TEXT, urlToImage TEXT, published TEXT)')
c.executemany('INSERT INTO coinsNews VALUES(?,?,?,?,?,?,?)', articlesList)
conn.commit()

# get table from database
def tableFromDatabase(database, table):
    conn = sqlite3.connect(database)  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT * FROM %s' % table)
    tableRows = c.fetchall()
    return tableRows

rows = tableFromDatabase('crypto.db', 'coinsNews')

# pass sql table to python list
coinsList = [list(row) for row in rows]

# normalize words
stop_words = set(stopwords.words('english') + ['cryptocurrency', 'cryptocurrencies', 'u', '000'])
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+') # takes only alphanum characters

def normalize(table):
    normal = []
    counts = []
    for row in table:
        word_tokens = tokenizer.tokenize(row[2])
        word_lower = [w.lower() for w in word_tokens]
        word_stem = [lemmatizer.lemmatize(w) for w in word_lower]
        filtered_row = [w for w in word_stem if not w in stop_words]
        normal.append(filtered_row)
        counts.append(Counter(filtered_row))
    return normal

normalized = normalize(coinsList)

def countW(normalized):
    allWords = []
    for row in normalized:
        for word in row:
            allWords.append(word)
    return Counter(allWords)

countsWords = countW(normalized)

# calculate tf-idf
def inverse_freq(all_documents):
    idf_values = {}
    all_tokens_set = set([item for row in all_documents for item in row])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, all_documents)
        idf_values[tkn] = math.log(len(all_documents) / (sum(contains_token)))
    return idf_values

#def tfidf(term, all_documents):
idf = inverse_freq(normalized)
tfidfs = {}
for term in idf:
       tfidf = idf[term]*countsWords[term]
       tfidfs[term]=tfidf

#sortedTfidfs = sorted(tfidfs.items(), key=lambda x:x[1], reverse = True)
sortVal = sorted(tfidfs.values(), reverse=True)
sortKey = sorted(tfidfs, key=tfidfs.get, reverse=True)

valKey = []
for i in range(len(sortKey)):
    row=[]
    row.append(sortKey[i])
    row.append(sortVal[i])
    valKey.append(row)

conn = sqlite3.connect('crypto.db')  # connection
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS sortedTFIDF')
c.execute('CREATE TABLE sortedTFIDF (word TEXT, value INTEGER)')
c.executemany('INSERT INTO sortedTFIDF VALUES(?,?)', valKey)
conn.commit()
conn.close()
