'''
Created on Feb 19, 2015

@author: cisstudent
'''

import DataPreparation.TweetProcess as tp
import Classifier.EventTweetClassifier as tc

class TweetFilter(object):
    def __init__(self,tweetCollection1,tweetCollection2):
        self._rawTweetCollection = tweetCollection1
        self._filteredTweetCollection = tweetCollection2
        self._hashDict = {}
        self._updateFilteredTweets()
        
    def _updateFilteredTweets(self):
        """method for updating the filtered tweets"""
        for entries in self._rawTweetCollection.find(timeout=False):
            tweetObj = tp.TweetInfoExtract(entries)
            tweetFeatures = tweetObj.features
            print tweetFeatures
            tweetHashVal = tweetFeatures["tweetHashValue"]
            if tweetHashVal in self._hashDict:
                pass
            else:
                self._hashDict[tweetHashVal] = 1
                infoScoreObj = tc.TweetScore(tweetFeatures)
                print entries["text"].encode("utf-8")
                print infoScoreObj.posScore 
                tweetInfoScore = infoScoreObj.posScore 
                tweetFeatures["initScore"] = tweetInfoScore
                entryId = self._filteredTweetCollection.insert(entries)
                self._filteredTweetCollection.update({"_id":entryId},{"$set":tweetFeatures})
            
        
        


#class InfoProcess(object):
#    def __init__(self,dbName,tweetCollection1,tweetCollection2,hashTagCollection,textUnitCollection,userCollection,urlCollection):
#        self._dbName = dbName
#        self._rawTweetCollection = tweetCollection1
#        self._filteredTweetCollection = tweetCollection2
#        self._hashTagCollection = hashTagCollection
#        self._textUnitCollection = textUnitCollection
#        self._userCollection = userCollection
#        self._urlCollection = urlCollection
#        
#    
#    def _updateTweetFeatures(self):
        