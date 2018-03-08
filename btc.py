#!/usr/bin/env python
# encoding: utf -8
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

#For help with learning how to stream the Twitter data, Marco Bonzanini's blog was used.  You can access his website and the pages of this tutorial here: (ADD WEBSITE)



#To access twitter data, must connect with a Twiiter account. 
#access_token = "252197958-qd0oMpuYd0VyB7Ghb0V3wzksS9heZkT3S2GfdSVs"
#access_secret = "WK1ZNHalvvPsNVC2ogL5l6ojo8FwtMeXsYIvjWzakb8PA"
#consumer_key = "vqusFEWFnnqEwqwXdAJnozuay"
#consumer_secret =   "Dbc4mcepoUGDBuscEtF4YDUYV8MF9wBcUztH5eXI8AOAl6uIVv"

access_token = "252197958-qo3dJNgCFpsKRMZIoqEryntbP6lvT0FfiRKc1wbB"
access_secret = "tiZZvccKXLyADGTeXFRdRgmpLC7gotnrjxjt3ymOjoh6S"
consumer_key = "BRmmLz9TbRl40w6LVr6vVzOIr"
consumer_secret =   "fe1WtWC4kizG5kBRaxHv9rPOn9k6gXMBF9fFae5Slx1IM2zE2r"


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
