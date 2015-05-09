'''
Created on Feb 17, 2015

@author: Debanjan Mahata
'''

import string
import hashlib
from datetime import datetime
from nltk import *

class LoadMiscTextUnits(object):
    """class for loading and getting the misc text units like slang words, feeling words, stop words, etc to be filtered out during processing of tweets"""
    def __init__(self):
        #english stopwords, gets the english stopwords from the file: "englishStopWords" stored in Resources folder
        self._englishStopwords = [lines.rstrip() for lines in open("C:\\Users\\cisstudent\\TwitterEventInfoRank\\TwitterEventInfoRank\\Resources\\englishStopwords")]
        
        #list of slang words used in twitter, gets the twitter slang words from the file: "TwitterSlangList.txt" stored in Resources folder
        self._twitterSlang = [lines.rstrip() for lines in open("C:\\Users\\cisstudent\\TwitterEventInfoRank\\TwitterEventInfoRank\\Resources\\TwitterSlangList.txt")]
        
        #general internet slang words, gets the general internet slang words from the file: "internetSlang.txt" stored in Resources folder
        self._internetSlang = [lines.rstrip().split(":")[0].lower() for lines in open("C:\\Users\\cisstudent\\TwitterEventInfoRank\\TwitterEventInfoRank\\Resources\\internetSlang.txt")]

        #feeling words from wefeelfine.org, gets the feeling words from the file: "feelingWords.txt" stored in Resources folder
        self._feelingWords = [lines.rstrip().split()[0] for lines in open("C:\\Users\\cisstudent\\TwitterEventInfoRank\\TwitterEventInfoRank\\Resources\\feelingWords.txt")]

        #masterList
        self._allSlangWords = self._internetSlang + self._twitterSlang
        
    @property
    def allSlangWords(self):
        """getter method for getting a list of slang words to be filtered out from the tweet text"""
        return self._allSlangWords
    
    @property
    def englishStopwords(self):
        """getter method for getting the list of english stopwords"""
        return self._englishStopwords
    
    @property
    def twitterSlang(self):
        """getter method for getting twitter specific slang words published by FBI in 2014"""
        return self._twitterSlang
    
    @property
    def feelingWords(self):
        """getter method for getting feeling words from wefeelfine.org"""
        return self._feelingWords
    
    @property
    def internetSlang(self):
        """getter method for getting the general slang words from the internet"""
        return self._internetSlang 
    
    
class TweetInfoProcess(object):
    """class for processing required information from a tweet"""
    def __init__(self,tweet):
        """Constructor method for TweetInfoExtract"""
        
        #json formatted tweet from twitter stream
        self._tweet = tweet
        
        #length of the tweet
        self._tweetLength = len(self._tweet["text"])
        
        #creating object for getting misc text units
        self._miscTextObj = LoadMiscTextUnits()
        
        #list of filtered hashtags present in the tweet (hashtags not containing slang words)
        self._filteredHashTags = [hashTag["text"] for hashTag in self._tweet["entities"]["hashtags"] if hashTag["text"].lower() not in self._miscTextObj.englishStopwords and hashTag["text"].lower() not in self._miscTextObj.feelingWords and hashTag["text"].lower() not in self._miscTextObj.allSlangWords and not self._isAllDigit(hashTag["text"].lower()) and len(hashTag["text"]) > 2]
                
        #number of filtered hashtags in the tweet
        self._noFilteredHashTags = len(self._filteredHashTags)
        
        #actual list of hashtags present in the tweet
        self._hashTags = [hashTag["text"] for hashTag in self._tweet["entities"]["hashtags"]]
        
        #actual number of hashtags present in the tweet
        self._noHashTags = len(self._hashTags)


        #list of user mentions in the tweet
        self._userMentions = [user["id"] for user in self._tweet["entities"]["user_mentions"]]
                
        #number of user mentions in the tweet
        self._noUserMentions = len(self._userMentions)
        
        #list of urls present in the tweet 
        self._urls = [u["expanded_url"] for u in self._tweet["entities"]["urls"]]

        #number of urls in the tweet
        self._noUrls = len(self._urls)

        #indicates whether the tweet contains url or not
        self._hasUrl = self._noUrls > 0
        
        #list of media elements 
        self._mediaElements = self._setMediaElements()
        
        #number of media elements in a tweet
        self._noMediaElements = len(self._mediaElements)

        #list of unigrams extracted from tweet text without filtering out the slangs and stopwords
        self._rawTokens = self._tweet["text"].split()
        
        #number of raw tokens
        self._noRawTokens = len(self._rawTokens)
        
        #list of cleaned filtered out unigram tokens of the tweet text
        self._tokens = self._setCleanedTweetTextTokens()
        
        #number of cleaned tokens
        self._noTokens = len(self._tokens)
        
        self._tokensForMd5Hash = self._getTokensForHashValueCalc()
        #list of nouns extracted from the tweet text
        self._nouns = [noun[0].lower() for noun in self._getTokenPOSTags() if noun[1][0] == "N" and noun[0].lower() in self._tokens]
        
        #number of nouns extracted from the tweet
        self._noNouns = len(self._nouns)
        
        #list of adjectives from the tweet text
        self._adjectives = [token[0].lower() for token in self._getTokenPOSTags() if token[1][0] == "J" and token[0].lower() in self._tokens]
                
        #number of adjectives in the tweet text
        self._noAdjectives = len(self._adjectives) 
        
        #list of verbs from the tweet text
        self._verbs = [token[0].lower() for token in self._getTokenPOSTags() if token[1][0] == "V" and token[0].lower() in self._tokens]
        
        #number of verbs in the tweet text
        self._noVerbs = len(self._verbs)
        
        #list of adverbs in the tweet text
        self._adverbs = [token[0].lower() for token in self._getTokenPOSTags() if token[1][0] == "R" and token[0].lower() in self._tokens]
        
        #number of adverbs in the tweet text
        self._noAdverbs = len(self._adverbs)
        
        #list of prepositions
        self._prepositions = [token[0].lower() for token in self._getTokenPOSTags() if token[1][0] == "IN" and token[0].lower() in self._tokens]
        
        #number of prepositions
        self._noPrepositions = len(self._prepositions)
        
        #list of pronouns
        self._pronouns = [token[0].lower() for token in self._getTokenPOSTags() if token[1] == "PRP" or token[1] == "PRP$" and token[0].lower() in self._tokens]
        
        #number of pronouns
        self._noPronouns = len(self._pronouns)
        
        #list of interjections in tweet text
        self._interjections = [token[0].lower() for token in self._getTokenPOSTags() if token[1] == "UH" and token[0].lower() in self._tokens]
        
        #number of interjections in tweet text
        self._noInterjections = len(self._interjections)
        
        #number of articles in tweet content
        self._noArticles = len([article for article in self._rawTokens if article.lower() in ["a","an","the"]])
              
        #number of special characters detected in the tweet text
        self._noSpecialChars = self._setnoOfSpecialCharacters()
        
        #number of unique characters used in the tweet text
        self._noUniqueChars = len(set(self._tweet["text"]))
        
        #number of feeling words expressing emotions detected in the tweet text
        self._noFeelingWords = len([word for word in self._rawTokens if word.lower() in self._miscTextObj.feelingWords])
        
        #number of slang words detected in the tweet text
        self._noSlangWords = len([word for word in self._rawTokens if word.lower() in self._miscTextObj.allSlangWords])
        
        #number of english stop words detected in the tweet text
        self._noEnglishStopWords = len([stopWord for stopWord in self._rawTokens if stopWord.lower() in self._miscTextObj.englishStopwords])
        
        #created time
        self._createdTime = datetime.strptime(self._tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
        #misspelling ratio
        #self.misspellingRatio = 0.0
        
        #md5 hashvalue of the tweet's text
        self._tweetHashValue = self._setTweetHashValue()
        
        #md5 hashvalue of filtered tweet tokens
        self._tweetTokenHashValue = None
        
        #indicates whether the tweet comes from a verified source or not
        self._isVerified = self._isTweetVerified()
        
        #retweet count of a tweet
        self._retweetCount = self._setRetweetCount()
        
        #favorite counts of the tweet
        self._favoriteCount = self._setFavoriteCount()
        
        #formality score of a tweet
        self._formality = self._setFormalityScore()
        
    def _setRetweetCount(self):
        """setter method for setting the number of times a tweet is retweeted"""
        retweetCount = 0
        if "retweeted_status" in self._tweet:
            retweetCount = self._tweet["retweeted_status"]["retweet_count"]
        return retweetCount
    
    def _setFavoriteCount(self):
        """setter method for setting the number of favorite counts for the tweet"""
        favoriteCount = 0
        if "retweeted_status" in self._tweet:
            favoriteCount = self._tweet["retweeted_status"]["favorite_count"]
        
        return favoriteCount


    
    def _isTweetVerified(self):
        """sets the value to 1 if the tweet comes from a verified source else 0"""
        if self._tweet["user"]["verified"] == True:
            return 1
        else:
            return 0
    
    def _isAscii(self,s):
        """detect if a string is Ascii or not"""
        for c in s:
            if c not in string.ascii_letters:
                return False
        return True
    
    def _isAllDigit(self,s):
        """detect if a string has all digits in it"""
        try:
            if "." in s:
                float(s)
            else:
                int(s)
            return True
        except ValueError:
            return False
        
    def _setnoOfSpecialCharacters(self):
        """setter method for setting the number of special characters used in the tweet. The characters like:
        @(used for user mention), #(used for hashtags) are not counted as special characters as they have their
        own significance in TwitterSphere"""
        
        noSpecialChars = 0
        for char in self._tweet["text"].encode("utf-8"):
            if char == "@" or char == "#" or char == " ":
                pass
            else:
                if char.isalnum() == False:
                    noSpecialChars += 1
                    
        return noSpecialChars
    
    def _setCleanedTweetTextTokens(self):
        """cleans tweet text and filters out all the hashtags, user mentions, and urls, also tokenizes the tweet text
        filters out all the tokens that contain english stop words or contains non-ascii non alphanumeric characters,
        also filters out the slang words"""
        
        
        stopWords =  self._miscTextObj.englishStopwords #gets the provided english stop words
        
        internetSlangWords =  self._miscTextObj.internetSlang   #gets the provided commonly used internet slang words
        
        twitterSlangWords = self._miscTextObj.twitterSlang
        
        wordTokens = self._rawTokens #splits the tweet text at whitespaces
        
        cleanedWordList = [] #container for cleaned tokens
        
        if wordTokens != []:
            for wrd in wordTokens:
                word = wrd.lower()
                if word.find("#") != -1 or word.find("@") != -1 or word.find("http") != -1:
                    pass
                else:
                    cleanWord = ''.join(e for e in word if e.isalpha())
                    if cleanWord != "" and cleanWord.lower() not in twitterSlangWords and cleanWord.lower() not in stopWords and cleanWord.lower() not in internetSlangWords and self._isAscii(cleanWord):
                        cleanedWordList.append(cleanWord)
       
        return cleanedWordList
    
    def _getTokensForHashValueCalc(self):
        """method for extracting the tokens from a tweet for hashvalue calculation"""
        wordTokens = self._rawTokens #splits the tweet text at whitespaces
        
        cleanedWordList = [] #container for cleaned tokens
        
        if wordTokens != []:
            for wrd in wordTokens:
                word = wrd.lower()
                if word.find("#") != -1 or word.find("@") != -1 or word.find("http") != -1:
                    pass
                else:
                    if word != "" and self._isAscii(word):
                        cleanedWordList.append(word)
       
        return cleanedWordList

        

    
    def _getTokenPOSTags(self):
        """getter method for annotating the tweet tokens with their corresponding POS tags. The default Penn Tree Bank POS tags
        are used"""
        tweetTokens = self._rawTokens
        taggedTokens = pos_tag(tweetTokens)
        return taggedTokens
    
    def _generateHashValue(self,tweetStr):
        """method for generating md5 code for a given string 'str'"""
        hash_object = hashlib.md5(tweetStr)
        return hash_object.hexdigest()

    
    def _setTweetHashValue(self):
        """setter method for setting md5 hash value of the tweet text"""
        tweetWords = "".join(self._tokensForMd5Hash)
        return self._generateHashValue(tweetWords)
    
    
    def _setMediaElements(self):
        """Setter method for setting the media elements extracted from a tweet"""
        mediaElems = []
        if "media" in self._tweet["entities"].keys():
            mediaElems = [u["expanded_url"] for u in self._tweet["entities"]["media"]]
        return mediaElems
    
    def _setFormalityScore(self):
        """setter method for getting the formality index of the tweet. Formality Index or F Measure of the tweet is calculated
        as follows:
        F-Measure = (noun frequency + adjective freq. + preposition freq. + article freq. - pronoun freq. - verb freq. - adverb freq. - interjection freq. + 100)/2

        Heylighen, F. and Dewaele, J.-M. (1999). Formality of language: definition, measurement
        and behavioral determinants. Technical report, Free University of Brussels."""
        
        tweetTokens = self._tweet["text"].split()
        if len(tweetTokens) == 0:
            formalityIndex = -100.0
        else:
            formalityIndex = float(((self._noNouns+self._noAdjectives+self._noPrepositions+self._noArticles)-(self._noPronouns+ self._noVerbs +self._noAdverbs +self._noInterjections)+100.0))/2.0
        return formalityIndex

        
       
    @property
    def filteredHashTags(self):
        """getter method for getting the filtered and cleaned hashtags that are not slang words, english stopwords, feeling words, all digits and contain more than 2 characters"""
        return self._filteredHashTags
    
    @property
    def noFilteredHashTags(self):
        """getter method for getting the number of filtered and cleaned hashtags that are not slang words, english stopwords, feeling words, all digits and contain more than 2 characters"""
        return self._noFilteredHashTags 
    
    @property
    def hashTags(self):
        """getter method for getting the list of raw hashtags used in a tweet"""
        return self._hashTags
    
    @property
    def noHashTags(self):
        """getter method for getting the number of raw hashtags used in a tweet"""
        return self._noHashTags
    
    @property
    def userMentions(self):
        """getter method for getting all the user mentions in a tweet"""
        return self._userMentions
    
    @property
    def noUserMentions(self):
        """getter method for getting the number of user mentions in a tweet"""
        return self._noUserMentions
    
    @property
    def rawTokens(self):
        """getter method for getting the raw unigram tokens extracted from a tweet"""
        return self._rawTokens
    
    @property
    def noRawTokens(self):
        """getter method for getting the number of raw unigram tokens extracted from a tweet"""
        return self._noRawTokens
    
    @property
    def noSpecialChars(self):
        """getter method for getting the number of special characters detected in a tweet"""
        return self._noSpecialChars
    
    @property
    def noUniqueChars(self):
        """getter method for getting the number of unique characters used in a tweet"""
        return self._noUniqueChars
    
    @property
    def tokens(self):
        """getter method for getting the cleaned tokens from a tweet after filtering out slang words"""
        return self._tokens
    
    @property
    def noTokens(self):
        """getter method for getting the number of cleaned tokens from a tweet"""
        return self._noTokens
        
    @property
    def nouns(self):
        """getter method for getting the nouns from a tweet"""
        return self._nouns

    @property
    def noNouns(self):
        """getter method for getting the number of nouns from a tweet"""
        return self._noNouns 
    
    @property
    def noFeelingWords(self):
        """getter method for getting the number of feeling words from a tweet"""
        return self._noFeelingWords
    
    @property
    def noSlangWords(self):
        """getter method for getting the number of slang words from a tweet"""
        return self._noSlangWords
    
    @property
    def noEnglishStopWords(self):
        """getter method for getting the number of english stop words from a tweet"""
        return self._noEnglishStopWords
    
    @property
    def adjectives(self):
        """getter method for getting the adjectives used in a tweet"""
        return self._adjectives
    
    @property
    def noAdjectives(self):
        """getter method for getting the number of adjectives in a tweet"""
        return self._noAdjectives
    
    @property
    def verbs(self):
        """getter method for getting the verbs in a tweet"""
        return self._verbs
    
    @property
    def noVerbs(self):
        """getter method for getting the number of verbs in a tweet"""
        return self._noVerbs 
    
    @property
    def adverbs(self):
        """getter method for getting the adverbs from a tweet"""
        return self._adverbs
    
    @property
    def noAdverbs(self):
        """getter method for getting the number of adverbs from a tweet"""
        return self._noAdverbs
    
    @property
    def prepositions(self):
        """getter method for getting the prepositions from a tweet"""
        return self._prepositions
    
    @property
    def noPrepositions(self):
        """getter method for getting the number of prepositions from a tweet"""
        return self._noPrepositions
    
    @property
    def pronouns(self):
        """getter method for getting the pronouns from a tweet"""
        return self._pronouns
    
    @property
    def noPronouns(self):
        """getter method for getting the number of pronouns from a tweet"""
        return self._noPronouns
    
    @property
    def interjections(self):
        """getter method for getting the interjections from a tweet"""
        return self._interjections
    
    @property
    def noInterjections(self):
        """getter method for getting the number of interjections from a tweet"""
        return self._noInterjections
    
    @property
    def createdTime(self):
        """getter method for getting the created time of a tweet"""
        return self._createdTime
    
    @property
    def isVerified(self):
        """getter method for getting the verification information of a tweet by twitter at the time of posting"""
        return self._isVerified
    
    @property
    def tweetHashValue(self):
        """getter method for getting the md5 hash value of the tweet"""
        return self._tweetHashValue
    
    @property
    def urls(self):
        """getter method for getting the urls shared in a tweet"""
        return self._urls
    
    @property
    def noUrls(self):
        """getter method for getting the number of urls shared in a tweet"""
        return self._noUrls
    
    @property
    def hasUrl(self):
        """getter method getting whether a tweet contains an url or not"""
        return self._hasUrl 
    
    @property
    def mediaElements(self):
        """getter method for getting the media elements shared in a tweet"""
        return self._mediaElements
    
    @property
    def noMediaElements(self):
        """getter method for getting the number of media elements shared in a tweet"""
        return self._noMediaElements
    
    @property
    def retweetCount(self):
        """getter method for getting the number of rewteets for a tweet"""
        return self._retweetCount
    
    @property
    def favoriteCount(self):
        """getter method for getting the favorite count of a tweet"""
        return self._favoriteCount 
    
    @property
    def tweetLength(self):
        """getter method for getting the length of the given tweet"""
        return self._tweetLength
    
    @property
    def formality(self):
        """getter method for getting the formality score of a tweet"""
        return self._formality 
    
    
class TweetInfoExtract(object):
    def __init__(self,tweet):
        
        self._tweet = tweet
        
        self._tweetObj = TweetInfoProcess(tweet)
        
        self._features = self._setTweetFeatures()
        
        
    def _setTweetFeatures(self):
        
        featureDict = {}
        
        featureDict["favoriteCount"] = self._tweetObj.favoriteCount
        featureDict["retweetCount"] = self._tweetObj.retweetCount
        featureDict["mediaElements"] = self._tweetObj.mediaElements
        featureDict["noMediaElements"] = self._tweetObj.noMediaElements
        featureDict["hasUrl"] = self._tweetObj.hasUrl
        featureDict["urls"] = self._tweetObj.urls
        featureDict["noUrls"] = self._tweetObj.noUrls
        featureDict["tweetHashValue"] = self._tweetObj.tweetHashValue 
        featureDict["isVerfied"] = self._tweetObj.isVerified
        featureDict["createdTime"] = self._tweetObj.createdTime 
        featureDict["interjections"] = self._tweetObj.interjections
        featureDict["noInterjections"] = self._tweetObj.noInterjections
        featureDict["prepositions"] = self._tweetObj.prepositions
        featureDict["noPrepositions"] = self._tweetObj.noPrepositions
        featureDict["adjectives"] = self._tweetObj.adjectives
        featureDict["noAdjectives"] = self._tweetObj.noAdjectives 
        featureDict["nouns"] = self._tweetObj.nouns 
        featureDict["noNouns"] = self._tweetObj.noNouns
        featureDict["verbs"] = self._tweetObj.verbs
        featureDict["noVerbs"] = self._tweetObj.noVerbs 
        featureDict["adverbs"] = self._tweetObj.adverbs
        featureDict["noAdverbs"] = self._tweetObj.noAdverbs 
        featureDict["pronouns"] = self._tweetObj.pronouns 
        featureDict["noPronouns"] = self._tweetObj.noPronouns
        featureDict["noEnglishStopWords"] = self._tweetObj.noEnglishStopWords
        featureDict["noFeelingWords"] = self._tweetObj.noFeelingWords
        featureDict["noSlangWords"] = self._tweetObj.noSlangWords 
        featureDict["tokens"] = self._tweetObj.tokens
        featureDict["noTokens"] = self._tweetObj.noTokens 
        featureDict["noUniqueChars"] = self._tweetObj.noUniqueChars 
        featureDict["noSpecialChars"] = self._tweetObj.noSpecialChars 
        featureDict["rawTokens"] = self._tweetObj.rawTokens 
        featureDict["noRawTokens"] = self._tweetObj.noRawTokens 
        featureDict["userMentions"] = self._tweetObj.userMentions 
        featureDict["noUserMentions"] = self._tweetObj.noUserMentions 
        featureDict["hashTags"] = self._tweetObj.hashTags 
        featureDict["noHashTags"] = self._tweetObj.noHashTags 
        featureDict["filteredHashTags"] = self._tweetObj.filteredHashTags 
        featureDict["noFilteredHashTags"] = self._tweetObj.noFilteredHashTags 
        featureDict["tweetLen"] = self._tweetObj.tweetLength 
        featureDict["formality"] = self._tweetObj.formality 
        
        return featureDict
        
    @property
    def features(self):
        """getter method for getting features extracted from a tweet"""
        return self._features 
         
    
        
        




