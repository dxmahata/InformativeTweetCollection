'''
Created on Feb 22, 2015

@author: Debanjan Mahata
'''

class StoreEventHashTag(object):
    def __init__(self, tweetCollection, hashTagCollection):
        self._tweetCollection = tweetCollection
        self._hashTagCollection = hashTagCollection
        
    def _getHashTagCount(self,hashTag):
        return self._tweetCollection.find({"entities.hashtags.text":hashTag}).count()
    
    def store(self):
        maxCount = 0.0
        for hashTag in self._tweetCollection.distinct("filteredHashTags"):
            hashTagCount = self._getHashTagCount(hashTag)
            if hashTagCount > maxCount:
                maxCount = hashTagCount
            self._hashTagCollection.insert({"text":hashTag,"tf":hashTagCount})
        for entries in self._hashTagCollection.find(timeout=False):
            self._hashTagCollection.update({"_id":entries["_id"]},{"$set":{"scaledTf":float(entries["tf"])/maxCount}})

        
