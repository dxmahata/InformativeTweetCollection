'''
Created on Feb 22, 2015

@author: cisstudent
'''
import AlchemyAPI as alchemy


class UrlMetaData(object):
    def __init__(self,url):
        self._url = url
        self._alchemyResp = alchemy.text_clean(flavor="url", data=url)
        self._fullUrl, self._urlText = self._parseAlchemyResponse()
        
    def _parseAlchemyResponse(self):
        if self._alchemyResp["status"] == "OK":
            return self._alchemyResp["url"], self._alchemyResp["text"]
        else:
            return None, None
        
    @property
    def url(self):
        return self._url 
    
    @property
    def fullUrl(self):
        return self._fullUrl
    
    @property
    def urlText(self):
        return self._urlText
