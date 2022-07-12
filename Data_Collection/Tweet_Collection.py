#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
June, 2022

@author: haleyroberts
"""

# Import packages
import tweepy
from tweepy import OAuthHandler
import pandas as pd
import re
import string
import time


###########################################################################
### Set up Twitter API info & Tweepy
###########################################################################

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



###########################################################################
### Method for getting information about a certain tweet 
###########################################################################

def get_tweet_data(tweet, column_names):

    ###############
    ### Get user mention data for tweet
    ###############
    
    # Instantiate empty lists to hold user mention data: id's & screen names
    user_mention_ids = []
    user_mention_screen_names = []

    # Get the user_mentions entity of the status
    user_mentions = tweet.entities['user_mentions']
    
    # Loop through the user mention data and append id & screen names to lists
    for user in user_mentions:
        user_mention_ids.append(user['id'])
        user_mention_screen_names.append(user['screen_name'])

    ###############
    ### Get hashtag data for tweet
    ###############
    
    # Instantiate empty list to hold hashtag data
    hashtags = []

    # Get the hashtag entity of the status
    hashtag_entity = tweet.entities['hashtags']
    
    # Loop through the hashtag data and append text to list
    for ht in hashtag_entity:
        hashtags.append(ht['text'])

    ###############
    ### Clean tweets
    ### Remove urls, hashtags, mentions, and non-English characters 
    ### Reference: https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
    ### Reference: https://stackoverflow.com/questions/42370508/how-to-delete-special-characters-such-as-ŒðŸ-from-tweets
    ###############
    
    # Get the text of the tweet
    text = tweet.full_text
    
    # Remove urls from tweets
    text_re = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)',
                         re.DOTALL)
    text_re2 = re.findall(text_re, text)
    for t in text_re2:
        text = text.replace(t[0], ', ') 
    
    # Remove hashtags & mentions from tweets
    prefixes = ['@','#']
    all_words = text.split()
    words_to_keep = []
    if len(all_words) >= 1:
        for word in all_words:
            if word[0] not in prefixes:
                words_to_keep.append(word)
    text = ' '.join(words_to_keep)
    
    # Remove non-English from tweets
    text = ''.join([char for char in text if ord(char) < 128])
        
    ###############
    ### Add all tweet attributes into dataframe
    ###############
    
    # Make list of tweet attributes to add to data frame
    list_tweets = [
                   # The time the status was posted.
                   tweet.created_at, #str(tweet.created_at.date()),
                   # The text of the status.
                   text, 
                   # The hashtags of the status
                   hashtags,
                   # The id's of the user_mentions of the status
                   user_mention_ids,
                   # The screen names of the user_mentions of the status
                   user_mention_screen_names,                      
                   # The number of retweets of the status.
                   tweet.retweet_count,
                   # The number of likes of the status.
                   tweet.favorite_count,
                   # The ID of the user being replied to.
                   tweet.in_reply_to_user_id,
                   # The screen name of the user being replied to
                   tweet.in_reply_to_screen_name,

                   # user : The User object of the poster of the status.
                   tweet.user.id,
                   tweet.user.screen_name,
                   tweet.user.name,
                   tweet.user.friends_count,
                   tweet.user.followers_count,
                   tweet.user.favourites_count,
                   tweet.user.verified,
                   tweet.user.statuses_count
                   ]

    # Convert list of tweet data into series
    series_tweets = pd.Series(list_tweets, 
                              index = column_names)
    
    # Return the tweet data
    return series_tweets
        


###########################################################################
### Method for collecting tweets
###########################################################################

def get_tweets(search_words, date_start, num_tweets, column_names, filename):
    
    # Get start time of tweet collection
    start_time = time.time()

    # Create dataframe to hold the twitter data, with specified headers
    tweet_data = pd.DataFrame(columns=column_names)
    
    # Get all tweets with specified search word
    tweets_all = tweepy.Cursor(api.search, 
                               q=search_words + " -filter:retweets",
                               lang="en",
                               since = date_start,
                               tweet_mode='extended').items(num_tweets)

    # Loop through tweets
    for tweet in tweets_all:
        
        # Get information about each tweet
        tweet_info = get_tweet_data(tweet, column_names)

        # Append tweet's information to dataframe
        tweet_data = tweet_data.append(tweet_info, ignore_index=True)
        
        # Add new tweet data to csv file
        tweet_data.to_csv(filename, index=False)
    
    # Get end time of tweet collection
    end_time = time.time()

    # Get time taken to collect tweets
    duration = round((end_time-start_time)/60,2)

    # Return the tweet data
    return tweet_data, duration



###########################################################################
### Collect Tweets
###########################################################################
    
# Specify dataframe column names
column_names = [
                # Data about tweet
                'created_at', 
                'text',
                'hashtags',
                'user_mention_ids',
                'user_mention_screen_names',
                'retweet_count',
                'favorite_count',
                'in_reply_to_user_id',
                'in_reply_to_screen_name',
                
                # Data about tweet creater
                'user_id',
                'user_screen_name',
                'user_name',
                'user_friends_count', 
                'user_followers_count',
                'user_favourites_count',
                'user_verfied',
                'user_statuses_count',
                ]

# Specify start date of gathering tweets
start_date = "2022-06-01"

# Specify number of tweets to collect
num_tweets = 10000

##############################
### Keyword: "starbucks"
##############################

# Indicate keyword to search
words_starbucks = "starbucks"

# Indicate filename to save data to
filename_starbucks = 'tweets_starbucks.csv'

# Call method to get tweets about keyword of interest
tweet_data_starbucks, duration = get_tweets(search_words = words_starbucks, 
                                            date_start = start_date,
                                            num_tweets = num_tweets,
                                            column_names = column_names,
                                            filename = filename_starbucks)

# Print total time for Starbucks tweet collections
print("Starbucks Collection Time: "+str(duration)+" mins")

##############################
### Keyword: "dunkin"
##############################

# Indicate keyword to search
words_dunkin = "dunkin"

# Indicate filename to save data to
filename_dunkin = 'tweets_dunkin.csv'

# Call method to get tweets about keyword of interest
tweet_data_dunkin, duration = get_tweets(search_words = words_dunkin, 
                                         date_start = start_date,
                                         num_tweets = num_tweets,
                                         column_names = column_names,
                                         filename = filename_dunkin)

# Get total time for Starbucks tweet collections
print("Dunkin' Collection Time: "+str(duration)+" mins")
