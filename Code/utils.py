import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import re
from nltk.stem import PorterStemmer

# -----------------
# Useful functions 
# -----------------

######################################
##  TEXT CLEANING & PREPROCESSING
######################################

def clean_tweets(tweet):

    # stopwords from nltk 
    stop_words = stopwords.words('english')

    # throw error if tweet is not correct type
    if type(tweet) == np.float:
        return "ERROR: wrong type"
    
    tweet = tweet.lower() # lowercase 
    tweet = re.sub(r"http\S+", "", tweet) # remove URLS
    tweet = re.sub(r"www.\S+", "", tweet) # remove URLS
    # TBD - KEEP @'S ?
    tweet = re.sub("@[A-Za-z0-9_]+","", tweet) # remove @'s 
    tweet = re.sub('[()!?]', ' ', tweet) # remove punctuation
    tweet = re.sub('\[.*?\]',' ', tweet) # remove punctuation
    tweet = re.sub("[^a-z0-9]"," ", tweet) #remove non alpha-numeric
    tweet = re.sub("\S*\d\S*", "", tweet).strip() # remove numbers + words with numbers 


    # tokenize words in tweet
    tweet_tokens = word_tokenize(tweet)

    # remove stopwords
    tweet = [w for w in tweet_tokens if not w in stop_words]

    # initialize stemmer
    ps = PorterStemmer()

    # stem each word in tweet
    tweet = [ps.stem(w) for w in tweet]

    # untokenize text
    tweet = TreebankWordDetokenizer().detokenize(tweet)

    # return cleaned tweets
    return tweet



def countWords(s):
  
    # Check if the string is null
    # or empty then return zero
    if s.strip() == "":
        return 0
  
    # Splitting the string
  
    words = s.split()
  
    return len(words)