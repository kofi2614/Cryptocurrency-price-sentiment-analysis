import time
import datetime
import requests
import sqlite3
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
from nltk.tokenize import word_tokenize 
import re 
from collections import Counter 
import nltk 
from nltk.corpus import stopwords 
import string 
from nltk import bigrams 
import vincent
import pandas 
from nltk.util import ngrams 
import matplotlib.pyplot as plt
import string
import numpy as np


#The purpose of this py file is to: pre-process the twitter data, count term frequencies, and visualize results.

#The commented text below can be used to check to see if the twitter data has successfully been uploaded in the json file and can be extracted.  It is also good to see how the data looks before you begin analysis and get familiar with the attributes
'''
data=json.loadwith open(open('twitter.json'))
fname='twitter.json'
with open('twitter.json', 'r') as f:
	line=f.readline() #read only the first tweet/line
	tweet=json.load(line) #load it as a Python dict
	print(json.dumps(tweet, indent=4)) #pretty-print
'''
#As Twitter data is unstructured and contains many things that are not words, they must be tokenized so that they are not included in our data that we will be mining.  There are common occurences in Tweets that must be omitted: emoticons, HTML tags, hashtag, @-mentions, URLS, numbers, etc.
emoticons_str=r"""
	(?:
		[:=;] #eyes
		[o0\-]? #nose
		[D\)\]\(\]/\\0pP] #mouth
	)"""
regex_str=[
	emoticons_str,
	r'<[^>]+>', #HTML tags
	r'(?:@[\w_]+)', # @mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", #hashtags
	r'http[s]?://(?:[a-z][0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
	r'(?:(?:\d+,?)+(?:\.?\d+)?)', #numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
	r'(?:[\w_]+)', #other words
	r'(?:\S)' #anything else
]
#regex_str is a list of possible patterns.  re.VERBOSE allows for ignoring spaces.  tokenize() puts all the tokens in a string and returns them as a list

tokens_re=re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re=re.compile(r'^'+emoticons_str+'$',re.VERBOSE| re.IGNORECASE)

def tokenize(s):
	return tokens_re.findall(s)

def preprocess(s, lowercase=False):
	tokens=tokenize(s)
	if lowercase:
		tokens=[token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

#the following code checks to see if the above code was used to correctly take out the above terms from the text.  Tweet("text") is the variable in which the Twitter data is stored in the JSON file
	
with open('bitcoin.json', 'r') as f:
	for line in f:		
		tweet=json.loads(line) #load it as a Python dict
		tokens=preprocess(tweet['text'])
		#print(preprocess(tweet['text']))

#the Counter() function is a term dictionary that counts frequecies and allows us to see the most common terms used
with open('bitcoin.json', 'r') as f:
	
	count_all=Counter()
	for line in f:
		tweet=json.loads(line) #create a list with all the terms	
		terms_all=[term for term in preprocess(tweet['text'])] #update the counter	
		count_all.update(terms_all)
		#print the 5 most frequent words 
	#print(count_all.most_common(10))
	
#Using what we learned in class about removing words that are common in the English language but do not provide any insight into the usage of our hashtag, stopwords was included to get rid of such terms
#Terms that are common in Twitter language were added


with open('bitcoin.json', 'r') as f:
	
	count_term=Counter()
	for line in f:
		tweet=json.loads(line) 

		punctuation=list(string.punctuation)
		stop=stopwords.words('english') + punctuation + ['rt', 'via', 'RT', ':', '1', 'contest', 'winner', 'referral', 'Retweet', '#bitcoin', '#Bitcoin', 'The', '...']
		terms_stop=[term for term in preprocess(tweet['text']) if term not in stop]
		
		#The code below is used to make our code more stringent on what we are analyzing

		terms_single=set(terms_all) #terms_single=count terms only once
		terms_hash=[term for term in preprocess(tweet['text']) #count hashtags only
			if term not in stop and
			term.startswith('#')]
		terms_only=[term for term in preprocess(tweet['text']) #count terms only ( no mentions)
			if term not in stop and
			not term.startswith(('@','u'))]
		
		count_term.update(terms_hash)
	#print(count_term.most_common(10))
#count_term.most_common(10))
#Using the code we leaned in class, we broke down usage of tuples commonly used together to see if that would provide us with any added insight



#to visualize the most common terms used, we put them in a histogram
word_freq=count_all.most_common(10)
labels, freq =zip(*word_freq)
data={'data': freq, 'x':labels}
bar=vincent.Bar(data,iter_idx='x')
bar.to_json('term_freq.json', html_out=True, html_path='chart.html')

#we also wanted to see how our chosen hashtag was used over time.  

def tweets():

	bitcointags=[]
	with open('bitcoin.json', 'r') as f:
		for line in f:
			tweet=json.loads(line) # as a Python dict
			terms_hash=[term for term in preprocess(tweet['text']) if term.startswith('#')] #look at '#' usage over time	
			if'#Bitcoin' in terms_hash:
				bitcointags.append(tweet['created_at']) #'created_at' is when the tweet was posted by the user
			
	ones=[1]*len(bitcointags) #a list of "1" to count the hashtags
	idx=pandas.DatetimeIndex(bitcointags) #the index of the series
	bitcointag=pandas.Series(ones, index=idx) #the actual series 
	per_minute=bitcointag.resample('1Min', how='sum').fillna(0) #tracking the frequency over time



	ethereumtags=[]
	with open('ethereum.json', 'r') as f:
		for line in f:
			tweet=json.loads(line) # as a Python dict
			terms_hash=[term for term in preprocess(tweet['text']) if term.startswith('#')] #look at '#' usage over time	
			if'#Ethereum' in terms_hash:
				ethereumtags.append(tweet['created_at']) #'created_at' is when the tweet was posted by the user
	ones=[1]*len(ethereumtags) #a list of "1" to count the hashtags
	idx=pandas.DatetimeIndex(ethereumtags) #the index of the series
	ethereumtag=pandas.Series(ones, index=idx) #the actual series 
	per_minute2=ethereumtag.resample('1Min', how='sum').fillna(0) #tracking the frequency over time


	both_data=dict(bitcointags=per_minute, ethereumtags=per_minute2)
	all_tags=pandas.DataFrame(data=both_data,
				index=per_minute.index )
	#all_tags=all_tags.resample('1Min', how='sum').fillna(0)
	#print(all_tags)
	#print(all_tags.iloc[0]['bitcointags'])
	aa = []
	for i in range(len(all_tags.index)):
		row = []
		row.append(str(all_tags.index[i]))
		row.append(all_tags.iloc[i]['bitcointags'])
		row.append(all_tags.iloc[i]['ethereumtags'])
		aa.append(row)
	return aa

def historical_data():
	response_his = requests.get("https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=1440")
	a = response_his.json()
	his = []
	for i in range(len(a[u'Data'])):
		data = []
		data.append(time.strftime("%D %H:%M", time.localtime(int(a[u'Data'][i][u'time']))))
		data.append(a[u'Data'][i][u'close'])
		his.append(data)
	return his
def current():
	response_current = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD")
	current_row = response_current.json()
	current = current_row[u'USD']
	return current
a = historical_data()
b = current()
bb = tweets()

d = ['BTC', b]
conn = sqlite3.connect('crypto.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS historical_data')
c.execute('DROP TABLE IF EXISTS current_data')
c.execute('CREATE TABLE historical_data(time TEXT, price FLOAT)')
c.executemany('INSERT INTO historical_data VALUES(?,?)', a)
c.execute('CREATE TABLE current_data(type TEXT, price FLOAT)')
c.execute('INSERT INTO current_data VALUES(?,?)', d)
c.execute('DROP TABLE IF EXISTS all_tags')
c.execute('CREATE TABLE all_tags(time TEXT, bitcoin FLOAT, ethereum FLOAT)'  )
c.executemany('INSERT INTO all_tags VALUES(?, ?, ?)', bb)
conn.commit()
#conn.close()
k = 0
while k <10000:
	#conn = sqlite3.connect('crypto.db')
	#c = conn.cursor()
	a_0 = historical_data()
	if a[len(a)-1][0] != a_0[len(a_0)-1][0]:
		a.append(a_0[len(a_0)-1])
		c.execute('INSERT INTO historical_data VALUES(?,?)', a[len(a)-1])
	#c.execute('SELECT MAX(time), price FROM historical_data')
	#print c.fetchall()
	#c.execute('SELECT COUNT(*) FROM historical_data')
	#print c.fetchall()
	#c.execute('SELECT * FROM historical_data')
	table = c.fetchall()
	#print len(table)
	b = current()
	d = ['BTC', b]
	c.execute('DELETE FROM current_data')
	c.execute('INSERT INTO current_data VALUES(?,?)', d)
	#c.execute('SELECT * FROM current_data')
	aa_0 = tweets() 
	print bb[len(bb)-1]
	if bb[len(bb)-1][0] == aa_0[len(aa_0)-3][0]:
		bb.append(aa_0[len(aa_0)-2])
		c.execute('INSERT INTO all_tags VALUES(?, ?, ?)', bb[len(bb)-1])
	c.execute('SELECT COUNT(*) from all_tags')
 	print c.fetchall()
	print (bb[len(bb)-5:len(bb)])
	print (aa_0[len(aa_0)-5:len(aa_0)])
	print (len(aa_0))
	print (len(bb))
	#print c.fetchall()
	k = k+1
	time.sleep(10)
	conn.commit()
conn.close()
