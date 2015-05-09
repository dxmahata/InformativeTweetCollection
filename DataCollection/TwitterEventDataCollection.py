'''
Created on Dec 23, 2014

@author: Debanjan Mahata
'''

from twython import TwythonStreamer
from TwitterAuthentication import keyList
from time import sleep
from random import randint
import EventInfoProcess.EventTweetProcess as tweetProcess
import EventInfoProcess.EventTweetClassifier as tweetClassify
import DataPreparation.TweetProcess as tp

from pymongo import MongoClient
#connecting to MongoDB database
mongoObj = MongoClient()
#setting the MongoDB database
db = mongoObj[""]
#setting the collection in the database for storing the Tweets
collection = db[""]




class MyStreamer(TwythonStreamer): 
    
    def on_success(self, data): 
        if data["lang"] == "en":
            tweet = data            
            tweetObj = tweetProcess.TweetProcess(tweet)
            tweetClassifyObj = tweetClassify.TweetScore()
            tweetClassifyObj.setTweetInstance(tweetObj.getDataInstanceForClassification())
            tweetInfoScore = tweetClassifyObj.getTweetPosScore()
            if tweetInfoScore > 0.9:
                print tweet["text"].encode("utf-8")
                print tweetInfoScore
            collection.insert(data)
            # Want to disconnect after the first result? 
            # self.disconnect() 
 
 
    def on_error(self, status_code, data): 
        sleep(randint(1,60))
        keys = keyList[randint(0,9)]
        stream = MyStreamer(keys["APP_KEY"],keys["APP_SECRET"],keys["OAUTH_TOKEN"],keys["OAUTH_TOKEN_SECRET"])
        stream.statuses.filter(track="#sxsw")
        
## Requires Authentication as of Twitter API v1.1 
while True:
    try:
        keys = keyList[randint(0,12)]
        stream = MyStreamer(keys["APP_KEY"],keys["APP_SECRET"],keys["OAUTH_TOKEN"],keys["OAUTH_TOKEN_SECRET"]) 
        stream.statuses.filter(track='#sxsw')
    except:
        continue


            
        
    
        
    
   



