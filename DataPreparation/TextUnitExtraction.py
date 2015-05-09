'''
Created on Feb 22, 2015

@author: cisstudent
'''
import AlchemyAPI as alchemy

class NamedEntityExtract(object):
    def __init__(self,tweetText):
        self._tweetText = tweetText
        self._alchemyResponse = alchemy.entities("text", data=tweetText, options={"sentiment":1})
        self._namedEntities = self._getNamedEntities()
        
    def _getNamedEntities(self):
        tweetEntities = []
        if self._alchemyResponse["status"] == "OK":
            namedEntities = self._alchemyResponse["entities"]
            if namedEntities != []:
                for entity in namedEntities:
                    if entity["type"] == "Hashtag" or entity["type"] == "TwitterHandle":
                        pass
                    else:
                        tweetEntities.append(entity["text"])
                        
        return tweetEntities
    
    @property
    def alchemyResponse(self):
        return self._alchemyResponse
    
    @property
    def namedEntities(self):
        return self._namedEntities 
    

class StoreEventTextUnits(object):
    def __init__(self, tweetCollection, textUnitCollection):
        self._tweetCollection = tweetCollection
        self._textUnitCollection = textUnitCollection
        
    def _getNounTextUnitCount(self,textUnit):
        return self._tweetCollection.find({"nouns":textUnit}).count()

    def _getNamedEntityTextUnitCount(self,textUnit):
        return self._tweetCollection.find({"namedEntities":textUnit}).count()

    
    def storeNounTextUnits(self):
        maxCount = 0.0
        for textUnit in self._tweetCollection.distinct("nouns"):
            textUnitCount = self._getHashTagCount(textUnit)
            if textUnitCount > maxCount:
                maxCount = textUnitCount
            self._hashTagCollection.insert({"text":textUnit,"tf":textUnitCount})
        for entries in self._hashTagCollection.find(timeout=False):
            self._hashTagCollection.update({"_id":entries["_id"]},{"$set":{"scaledTf":float(entries["tf"])/maxCount}})
            
    def storeNamedEntityTextUnits(self):
        maxCount = 0.0
        for textUnit in self._tweetCollection.distinct("namedEntities"):
            textUnitCount = self._getHashTagCount(textUnit)
            if textUnitCount > maxCount:
                maxCount = textUnitCount
            self._hashTagCollection.insert({"text":textUnit,"tf":textUnitCount})
        for entries in self._hashTagCollection.find(timeout=False):
            self._hashTagCollection.update({"_id":entries["_id"]},{"$set":{"scaledTf":float(entries["tf"])/maxCount}})

