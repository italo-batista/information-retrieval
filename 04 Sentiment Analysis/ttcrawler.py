import tweepy
import csv
import pandas as pd
import configparser

# https://twitter.com/search-home#

config = configparser.ConfigParser()
config.read('config.ini')

access_token = config['DEFAULT']['access_key']
access_token_secret = config['DEFAULT']['access_secret']
consumer_key = config['DEFAULT']['consumer_key']
consumer_secret = config['DEFAULT']['consumer_secret']
                                  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

csv_file = open('tweets_bolsonaro.csv', 'a')
csv_writer = csv.writer(csv_file)

for tweet in tweepy.Cursor(api.search,q="#bolsonaro ❤️",count=100,
                           lang="pt",
                           since="2018-01-01").items():
    print (tweet.created_at, tweet.text)
    csv_writer.writerow([tweet.created_at, tweet.text.encode('utf-8')])
