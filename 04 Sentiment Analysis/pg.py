#!/usr/bin/env python
#
# http://socialmedia-class.org/twittertutorial.html
# https://paulovasconcellos.com.br/aprenda-a-fazer-um-analisador-de-sentimentos-do-twitter-em-python-3979454f2d0d
# https://apps.twitter.com/app/15664040/keys
#
#-----------------------------------------------------------------------
# twitter-search
#  - performs a basic keyword search for tweets containing the keywords
#-----------------------------------------------------------------------

from twitter import *

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
import sys
sys.path.append(".")
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(config['DEFAULT']['access_key'],
                  config['DEFAULT']['access_secret'],
                  config['DEFAULT']['consumer_key'],
                  config['DEFAULT']['consumer_secret']))

#-----------------------------------------------------------------------
# perform a basic search 
# Twitter API docs:
# https://dev.twitter.com/rest/reference/get/search/tweets
#-----------------------------------------------------------------------
query = twitter.search.tweets(q = "bolsonaro")

#-----------------------------------------------------------------------
# How long did this query take?
#-----------------------------------------------------------------------
print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))

#-----------------------------------------------------------------------
# Loop through each of the results, and print its content.
#-----------------------------------------------------------------------
for result in query["statuses"]:
    print("(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"]))
    
import csv
# Open/Create a file to append data
csv_file = open('tweets.csv', 'a')
csv_writer = csv.writer(csv_file)

for tweet in query["statuses"]:
    csv_writer.writerow([tweet["created_at"], tweet["text"].encode('utf-8')])    
