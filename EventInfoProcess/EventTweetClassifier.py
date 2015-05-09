'''
Created on Dec 24, 2014

@author: Debanjan Mahata
'''
import numpy as np
from sklearn.externals import joblib
model_clone = joblib.load('C:\\Users\\cisstudent\\TwitterEventInfoRank\\TwitterEventInfoRank\\EventInfoProcess\\my_model.pkl')

class TweetScore:
    def __init__(self):
        self.tweetInstance = []
        self.posScore = 0.0
        self.negScore = 0.0
        
    def setTweetScore(self):
        probScores = model_clone.predict_proba(np.array(self.getTweetInstance()))
        self.posScore = probScores[0][1]
        self.negScore = probScores[0][0]

        
    def setTweetInstance(self,tweetInstance):
        self.tweetInstance = tweetInstance
        self.setTweetScore()
        
    def getTweetInstance(self):
        return self.tweetInstance
    
        
    def getTweetPosScore(self):
        return self.posScore
    
    def getTweetNegScore(self):
        return self.negScore
    
    
        
    