#!/usr/bin/env python
# encoding: utf -8
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

#For help with learning how to stream the Twitter data, Marco Bonzanini's blog was used.  You can access his website and the pages of this tutorial here: (ADD WEBSITE)



access_token = "YOUR TWITTER ACCESS TOKEN"
access_secret = "YOUR TWITTER ACCESS SECRET"
consumer_key = "YOUR TWITTER CONSUMER KEY"
consumer_secret =   "YOUR TWITTER CONSUMER SECRET"


auth=OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#Tweepy= a Python library for accessing the Twitter API.  "api" allows us to use the data from Twitter
api=tweepy.API(auth)

# This allows for having the connection open and available if we want to keep streaming tweets.  We are saving the tweets to a json file called "trial.json'.  To narrow the scope of this project, we have closen to focus on the hashtag 'Bitcoin'.  However, if we wanted to look at another hashtag, this can easily be changed.

class MyListener(StreamListener):
	def on_data(self,data):
		try:
			with open('bitcoin.json','a') as f:
				f.write(data)
				return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self,status):
		print(status)
		return True

twitter_stream=Stream(auth,MyListener())
twitter_stream.filter(track=['#Bitcoin'])

#To check the output of this hashtag, uncomment the print statement below.  To get a good amount of twitter data, must let the stream.py run for some time.  
#print('Streaming Twitter data. To stop streaming, press Ctrl and C', twitter_stream)
