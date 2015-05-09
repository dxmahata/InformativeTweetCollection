'''
Created on Dec 23, 2014

@author: Debanjan Mahata
'''

import string
import hashlib
from datetime import datetime
from nltk import *

class TweetProcess:
    """class for processing the textual content of a tweet"""
    def __init__(self,tweet):
        """Constructor method for TweetTextProcess"""
        
        #json formatted tweet from twitter stream
        self.tweet = tweet
        
        #english stopwords, gets the english stopwords from the file: "englishStopWords" stored in utilFiles folder
        self.english_stopwords = [lines.rstrip() for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\englishStopwords")]
        
        #list of slang words used in twitter, gets the twitter slang words from the file: "TwitterSlangList.txt" stored in utilFiles folder
        self.twitter_slang = [lines.rstrip() for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\TwitterSlangList.txt")]
        
        #general internet slang words, gets the general internet slang words from the file: "internetSlang.txt" stored in utilFiles folder
        self.internet_slang = [lines.rstrip().split(":")[0].lower() for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\internetSlang.txt")]
        
        #feeling words from wefeelfine.org, gets the feeling words from the file: "feelingWords.txt" stored in utilFiles folder
        self.feelingWords = [lines.rstrip().split()[0] for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\feelingWords.txt")]
        
        #number of filtered hashtags in the tweet
        self.noHashTags = 0
        
        #number of user mentions in the tweet
        self.noUserMentions = 0
        
        #number of urls in the tweet
        self.noUrls = 0
        
        #actual list of hashtags present in the tweet
        self.rawHashTags = []
        
        #actual number of hashtags present in the tweet
        self.noRawHashTags = 0
        
        #list of urls present in the tweet 
        self.urls = []
        
        #list of nouns extracted from the tweet text
        self.nouns = []
        
        #list of cleaned unigram tokens of the tweet text
        self.tokens = []
        
        #number of special characters detected in the tweet text
        self.noSpecialChars = 0
        
        #length of the tweet
        self.tweetLength = 0
        
        #number of unique characters used in the tweet text
        self.noUniqueChars = 0
        
        #number of feeling words expressing emotions detected in the tweet text
        self.noFeelingWords = 0
        
        #number of slang words detected in the tweet text
        self.noSlangWords = 0
        
        #number of english stop words detected in the tweet text
        self.noEnglishStopWords = 0
        
        #list of unigrams extracted from tweet text without filtering out the slangs and stopwords
        self.rawTokens = []
        
        #misspelling ratio
        #self.misspellingRatio = 0.0
        
        #md5 hashvalue of the tweet's text
        self.tweetHashValue = 0.0
        
        #indicates whether the tweet comes from a verified source or not
        self.isVerified = 0
        
        #indicates whether the tweet contains url or not
        self.hasUrl = 0
        
        #tweet feature dictionary
        self.featureDict = {}
        
        #retweet count of a tweet
        self.retweetCount = 0
        
        #favorite counts of the tweet
        self.favoriteCount = 0
        
        #number of extracted tokens
        self.noTokens = 0
        
        #initial informativeness score of a tweet
        self.initInfoScore = 0.0
        
        self.setterMethodCalls()

        
    def setterMethodCalls(self):
        #called methods for setting the instance variables
        #calling method for setting the length of the tweet text
        self.setTweetLength()
        
        #calling method for setting the list of raw unigram tokens extracted from the tweet text
        self.setTweetRawTokens()
        
        #calling method for setting the list of cleaned unigrams extracted from the tweet text
        self.setCleanedTweetTextTokens()
        
        #calling method for setting the list of raw hashtags in tweet text
        self.setTweetRawHashTags()
        
        
        #calling method for setting the number of raw hashtags in a tweet
        self.setNoRawHashTags()
        
        #calling method for setting the list of nouns extracted from tweet text
        self.setNouns()
        
        #calling method for setting the number of user mentions in the tweet
        self.setNoUserMentions()
        
        #calling method for setting the list of urls in the tweet
        self.setTweetUrls()
        

        #calling method for setting the number of special characters detected in the tweet text
        self.noOfSpecialCharacters()
        
        #calling method for setting the number of unique characters detected in the tweet text
        self.setNoUniqueChars()
        
        #calling method for setting the number of feeling words detected in the tweet text
        self.setNoFeelingWords()
        
        #calling method for setting the number of slang words detected in the tweet text
        self.setNoSlangWords()
        
        #calling method for setting the number of stop words detected in the tweet text
        self.setNoEnglishStopWords()
        
        
        #calling method for setting the number of urls present in the tweet
        self.setNoOfUrls()
        
        #calling method for setting the misspelling ratio
        #self.setMisSpellingRatio()
        
        #calling method for knowing if the tweet comes from a verified source
        self.isTweetVerified()
        
        #calling method for setting the md5 hash value of the tweet's text
        self.setTweetHashValue()
        
        #calling method for setting the retweet count
        self.setRetweetCount()
        
        #calling method for setting the favorite count
        self.setFavoriteCount()
        
        #calling method for setting the number of tokens extracted from the tweet
        self.setNoOfTokens()
        
        #calling method for setting the tweet's feature dictionary
        self.setTweetFeatureDict()
                
#        #calling method for setting initial informativeness score of the tweet
#        self.setTweetInitScore()
        
    def setNoEnglishStopWords(self):
        """setter method for detecting the english stop words from the tweet text"""
        tweetTokens = self.tweet["text"].split()
        self.noEnglishStopWords = len([stopWord for stopWord in tweetTokens if stopWord.lower() in self.english_stopwords])   
     
    def getNoEnglishStopWords(self):
        """getter method for getting the number of english stop words detected in the tweet text"""
        return self.noEnglishStopWords
        
    def setNoSlangWords(self):
        """setter method for detecting the english slang words from the tweet text"""
        tweetTokens = self.tweet["text"].split()
        self.noSlangWords = len([slangWord for slangWord in tweetTokens if slangWord.lower() in self.twitter_slang or slangWord.lower() in self.internet_slang ])   
     
    def getNoSlangWords(self):
        """getter method for getting the number of english slang words detected in the tweet text"""
        return self.noSlangWords
    
    def setNoFeelingWords(self):
        """setter method for detecting the english feeling words from the tweet text text"""
        tweetTokens = self.tweet["text"].split()
        self.noFeelingWords = len([feelingWord for feelingWord in tweetTokens if feelingWord.lower() in self.feelingWords])
       
    def getNoFeelingWords(self):
        """getter method for getting the number of english feeling words detected in the tweet text"""
        return self.noFeelingWords
    
    def isAscii(self,s):
        """detect if a string is Ascii or not"""
        for c in s:
            if c not in string.ascii_letters:
                return False
        return True
    
    def getTweet(self):
        """getter method for getting the tweet"""
        return self.tweet
    
    def setTweet(self,tweet):
        """setter method for setting the tweet"""
        self.tweet = tweet
        
    def getTweetRawText(self):
        """getter method for getting the raw text of the tweet"""
        return self.tweet["text"]
    
    def setTweetRawHashTags(self):
        """setter method for setting the list of all the hashtags used in the tweet"""
        self.rawHashTags = [hashTag["text"] for hashTag in self.tweet["entities"]["hashtags"]]
        
    def getTweetRawHashTags(self):
        """getter method for getting a list of all the hashtags used in the tweet"""
        return self.rawHashTags
    
    def setNoUserMentions(self):
        """setter method for setting the number of user mentions in the tweet"""
        self.noUserMentions = len(self.tweet["entities"]["user_mentions"])
        
    def getNoUserMentions(self):
        """getter method for getting the number of user mentions in the tweet"""
        return self.noUserMentions

    def setNoRawHashTags(self):
        """setter method for setting the number of hashtags used in the tweet"""
        self.noRawHashTags = len(self.rawHashTags)
        
    def getNoRawHashTags(self):
        """getter method for getting the number of hashtags used in the tweet"""
        return self.noRawHashTags
    
    def setTweetUrls(self):
        """setter method for setting the list of urls used in the tweet"""
        self.urls = [u["url"] for u in self.tweet["entities"]["urls"]]
        
    def getTweetUrls(self):
        """getter method for getting the list of urls used in the tweet"""
        return self.urls
        
    def setNoOfUrls(self):
        """setter method for setting the number of urls used in the tweet"""
        self.noUrls = len(self.urls)
        
    def getNoOfUrls(self):
        """getter method for getting the number of urls used in the tweet"""
        return self.noUrls
    
    def setEnglishStopWords(self,stopwordFile="C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\englishStopwords"):
        """setter method for setting the list of english stop words"""
        englishStopwords = [lines.rstrip() for lines in open(stopwordFile)]
        self.english_stopwords = englishStopwords
        
    def getEnglishStopWords(self):
        """getter method for getting the list of english stop words"""
        return self.english_stopwords
    
    def setInternetSlangWords(self,internetSlangFile="C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\internetSlang.txt"):
        """setter method for setting the list of general internet slang words"""
        self.internet_slang = [lines.rstrip().split(":")[0].lower() for lines in open(internetSlangFile)]
    
    def getInternetSlangWords(self):
        """getter method for getting the list of general internet slang words"""
        return self.internet_slang
    
    def setTwitterSlangWords(self, twitterSlangFile="C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\TwitterSlangList.txt"):
        """setter method for setting the list of twitter slang words published by FBI"""
        self.twitter_slang = [lines.rstrip() for lines in open(twitterSlangFile)]
        
    def getTwitterSlangWords(self):
        """getter method for getting the list of twitter slang words published by FBI"""
        return self.twitter_slang
    
    def setCleanedTweetTextTokens(self):
        """cleans tweet text and filters out all the hashtags, user mentions, and urls, also tokenizes the tweet text
        filters out all the tokens that contain english stop words or contains non-ascii non alphanumeric characters,
        also filters out the slang words"""
        
        
        stopWords = self.english_stopwords #gets the provided english stop words
        
        internetSlangWords = self.internet_slang #gets the provided commonly used internet slang words
        
        twitterSlangWords = self.twitter_slang
        
        wordTokens = self.rawTokens #splits the tweet text at whitespaces
        
        cleanedWordList = [] #container for cleaned tokens
        
        if wordTokens != []:
            for wrd in wordTokens:
                word = wrd.lower()
                if word.find("#") != -1 or word.find("@") != -1 or word.find("http") != -1:
                    pass
                else:
                    cleanWord = ''.join(e for e in word if e.isalpha())
                    if cleanWord != "" and cleanWord.lower() not in twitterSlangWords and cleanWord.lower() not in stopWords and cleanWord.lower() not in internetSlangWords and self.isAscii(cleanWord):
                        cleanedWordList.append(cleanWord)
       
        self.tokens = cleanedWordList
        
        
    def setTweetRawTokens(self):
        """setter method for setting the list of raw unigram tokens extracted from the tweet"""
        self.rawTokens = self.tweet["text"].split()
        
    def noOfSpecialCharacters(self):
        """setter method for setting the number of special characters used in the tweet. The characters like:
        @(used for user mention), #(used for hashtags) are not counted as special characters as they have their
        own significance in TwitterSphere"""
        
        noSpecialChars = 0
        for char in self.tweet["text"].encode("utf-8"):
            if char == "@" or char == "#" or char == " ":
                pass
            else:
                if char.isalnum() == False:
                    noSpecialChars += 1
        self.noSpecialChars = noSpecialChars
    
    def getNoOfSpecialCharacters(self):
        """getter method for getting the number of special characters used in the tweet"""
        return self.noSpecialChars
    
    def getTokenPOSTags(self):
        """getter method for annotating the tweet tokens with their corresponding POS tags. The default Penn Tree Bank POS tags
        are used"""
        tweetTokens = self.rawTokens
        taggedTokens = pos_tag(tweetTokens)
        return taggedTokens
    
    def getNoOfArticles(self):
        """getter method for getting the number of articles of english grammar "a","an","the" detected in the tweet"""
        return len([article for article in self.rawTokens if article.lower() in ["a","an","the"]])
    
    
    def setNouns(self):
        """setter method for setting the list of nouns extracted from the tweet text"""
        self.nouns = [noun[0].lower() for noun in self.getTokenPOSTags() if noun[1][0] == "N" and noun[0].lower() in self.tokens]
        
    def getNouns(self):
        """getter method for getting the nouns extracted from the tweet text"""
        return self.nouns
        
    def getNoOfNouns(self):
        """getter method for getting the number of nouns extracted from the tweet""" 
        return len([noun for noun in self.getTokenPOSTags() if noun[1][0] == "N"])

    def getNoOfAdjectives(self):
        """getter method for getting the number of adjectives extracted from the tweet"""
        return len([token for token in self.getTokenPOSTags() if token[1][0] == "J"])

    def getNoOfPrepositions(self):
        """getter method for getting the number of prepositions extracted from the tweet"""
        return len([token for token in self.getTokenPOSTags() if token[1][0] == "IN"])

    def getNoOfPronouns(self):
        """getter method for getting the number of pronouns extracted from the tweet"""
        return len([token for token in self.getTokenPOSTags() if token[1] == "PRP" or token[1] == "PRP$"])

    def getNoOfVerbs(self):
        """getter method for getting the number of verbs extracted from the tweet"""
        return len([token for token in self.getTokenPOSTags() if token[1][0] == "V"])

    def getNoOfAdVerbs(self):
        """getter method for getting the number of adverbs extracted from the tweet"""
        return len([token for token in self.getTokenPOSTags() if token[1][0] == "R"])

    def getNoOfInterjections(self):
        """getter method for getting the number of interjections extracted from the tweet"""
        return len([token for token in self.getTokenPOSTags() if token[1] == "UH"])

    def getTweetTextFormality(self):
        """getter method for getting the formality index of the tweet. Formality Index or F Measure of the tweet is calculated
        as follows:
        F-Measure = (noun frequency + adjective freq. + preposition freq. + article freq. - pronoun freq. - verb freq. - adverb freq. - interjection freq. + 100)/2

        Heylighen, F. and Dewaele, J.-M. (1999). Formality of language: definition, measurement
        and behavioral determinants. Technical report, Free University of Brussels."""
        
        tweetTokens = self.tweet["text"].split()
        if len(tweetTokens) == 0:
            formalityIndex = 0.0
        else:
            formalityIndex = float(((self.getNoOfNouns()+self.getNoOfAdjectives()+self.getNoOfPrepositions()+self.getNoOfArticles())-(self.getNoOfPronouns()+self.getNoOfVerbs()+self.getNoOfAdVerbs()+self.getNoOfInterjections()))+100.0)/2.0
        return formalityIndex
    
    def setTweetLength(self):
        """setter method for setting the length of the tweet, which is the number of characters in the tweet"""
        self.tweetLength = len(self.tweet["text"])
        
    def getTweetLength(self):
        """getter method for getting the length of the tweet"""
        return self.tweetLength
    
    def setNoUniqueChars(self):
        """setter method for setting the number of unique characters in the tweet"""
        self.noUniqueChars = len(set(self.tweet["text"]))
        
    def getNoUniqueChars(self):
        """getter method for getting the number of unique characters in the tweet"""
        return self.noUniqueChars

    def generateHashValue(self,tweetStr):
        """method for generating md5 code for a given string 'str'"""
        hash_object = hashlib.md5(tweetStr)
        return hash_object.hexdigest()
    
    def setTweetHashValue(self):
        """setter method for setting md5 hash value of the tweet text"""
        tweetWords = "".join(self.tokens)
        self.tweetHashValue = self.generateHashValue(tweetWords)
        
    def getTweetHashValue(self):
        """getter method for getting the hash value of a tweet"""
        return self.tweetHashValue
    
    def isTweetVerified(self):
        """sets the value to 1 if the tweet comes from a verified source else 0"""
        if self.tweet["user"]["verified"] == True:
            self.isVerified = 1
        else:
            self.isVerified = 0
            
    def getTweetVerified(self):
        """getter method to get if the tweet is verified or not"""
        return self.isVerified
            
    def tweetHasUrl(self):
        """setter method for hasUrl. If tweet has url then 1 else 0"""
        if self.urls != []:
            self.hasUrl = 1
        else:
            self.hasUrl = 0
            
    def getCreatedTime(self):
        """gets the tweets post time in python datetime format"""
        return datetime.strptime(self.tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')

    def setRetweetCount(self):
        """setter method for setting the number of times a tweet is retweeted"""
        retweetCount = 0
        if "retweeted_status" in self.tweet:
            retweetCount = self.tweet["retweeted_status"]["retweet_count"]
        self.retweetCount = retweetCount
#        self.retweetCount = self.tweet["retweet_count"]
        
    def getRetweetCount(self):
        """getter method for getting the retweet count of a tweet"""
        return self.retweetCount
        
    def setFavoriteCount(self):
        """setter method for setting the number of favorite counts for the tweet"""
        favoriteCount = 0
        if "retweeted_status" in self.tweet:
            favoriteCount = self.tweet["retweeted_status"]["favorite_count"]
        
        self.favoriteCount = favoriteCount
#        self.favoriteCount = self.tweet["favorite_count"]
        
    def getFavoriteCount(self):
        """getter method for getting the favorite count of the tweet"""
        return self.favoriteCount
    
    def setNoOfTokens(self):
        """setter method for setting the number of tokens extracted from the tweet"""
        self.noTokens = len(self.tokens)
        
    def getNoOfTokens(self):
        """getter method for getting the number of tokens extracted from the tweet"""
        return self.noTokens
    
    def setTweetFeatureDict(self):
        """"sets the feature dictionary for the tweet"""
        self.featureDict = {"tweetUrls":self.getTweetUrls(),"md5Hash":self.getTweetHashValue(),"createdTime":self.getCreatedTime(),"tokens":self.tokens,"nouns":self.nouns,"favoriteCount":self.getFavoriteCount(),"retweetCount":self.getRetweetCount(),"formality":self.getTweetTextFormality(),"isTweetVerified":self.getTweetVerified(),"hasUrl":self.hasUrl,"noWords":self.getNoOfTokens(),"noStopWords":self.getNoEnglishStopWords(),"noFeelingWords":self.getNoFeelingWords(),"noSlangWords":self.getNoSlangWords(),"noHashTags":self.getNoRawHashTags(),"noUserMentions":self.getNoUserMentions(),"tweetLen":self.getTweetLength(),"noUrls":self.getNoOfUrls(),"uniqueChars":self.getNoUniqueChars(),"noSpecialChars":self.getNoOfSpecialCharacters()}
    
    def getTweetFeatureDict(self):
        """getter method for getting the tweet's features"""
        return self.featureDict 

    
    def getDataInstanceForClassification(self):
        """getter method for getting the features of a tweet for initial classification as informative/non-informative"""
        dataInstance = [1.0]
        if self.featureDict["noUrls"] > 0:
            dataInstance.append(float(1.0))
        else:
            dataInstance.append(float(0.0))
        dataInstance.append(float(self.featureDict["noWords"])/20.0)
        dataInstance.append(float(self.featureDict["noStopWords"])/21.0)
        dataInstance.append(float(self.featureDict["noFeelingWords"])/7.0)
        dataInstance.append(float(self.featureDict["noSlangWords"])/7.0)
        dataInstance.append(float(self.featureDict["noHashTags"])/17.0)
        dataInstance.append(float(self.featureDict["noUserMentions"])/8.0)
        dataInstance.append(float(self.featureDict["noUrls"])/3.0)
        dataInstance.append(float(self.featureDict["tweetLen"])/140.0)
        dataInstance.append(float(self.featureDict["uniqueChars"])/140.0)
        dataInstance.append(float(self.featureDict["noSpecialChars"])/140.0)
        dataInstance.append(float(self.featureDict["favoriteCount"])/13802.0)
        dataInstance.append(float(self.featureDict["retweetCount"])/41633.0)
        dataInstance.append(float(self.featureDict["formality"])/63.5)
        dataInstance.append(float(self.featureDict["isTweetVerified"]))
        
        return dataInstance
    
    
class LoadSlang:
    """class for loading and getting the slang words to be filtered out during processing of tweets"""
    def __init__(self):
        #english stopwords, gets the english stopwords from the file: "englishStopWords" stored in utilFiles folder
        self.english_stopwords = [lines.rstrip() for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\englishStopwords")]
        
        #list of slang words used in twitter, gets the twitter slang words from the file: "TwitterSlangList.txt" stored in utilFiles folder
        self.twitter_slang = [lines.rstrip() for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\TwitterSlangList.txt")]
        
        #general internet slang words, gets the general internet slang words from the file: "internetSlang.txt" stored in utilFiles folder
        self.internet_slang = [lines.rstrip().split(":")[0].lower() for lines in open("C:\\Users\\cisstudent\\EIIMWorkspace\\SeenAPI\\utilFiles\\internetSlang.txt")]

        #masterList
        self.slangWords = self.english_stopwords+self.twitter_slang+self.internet_slang
        
    def getSlang(self):
        """getter method for getting a list of slang words to be filtered out from the tweet text"""
        return self.slangWords

    





        




        