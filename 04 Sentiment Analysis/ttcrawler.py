import tweepy
import csv
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

access_token = config['DEFAULT']['access_key']
access_token_secret = config['DEFAULT']['access_secret']
consumer_key = config['DEFAULT']['consumer_key']
consumer_secret = config['DEFAULT']['consumer_secret']
                                  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

csv_file = open('tweets_test.csv', 'a')
csv_writer = csv.writer(csv_file, delimiter=';')
csv_writer.writerow(["text"])

cursor = tweepy.Cursor(api.search,q="#eleicoes2018", count=100, lang="pt", since="2018-01-01")
for tweet in cursor.items():
    print(tweet.text)
    csv_writer.writerow([tweet.text])