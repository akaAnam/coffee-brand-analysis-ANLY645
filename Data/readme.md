# Datasets 

Datasets in this folder:

  * **starbucks.csv / dunkin.csv**: all tweet data pulled from Tweepy API with cleaned text data, and sentiment data
  
 * **starbucks_TDM.csv / dunkin_TDM.csv**: Term Document Matrix of all tweets. Will use for edges 

 * **starbucks_hashtag_TDM.csv / dunkin_hashtag_TDM.csv**: Term Document Matrix of all hashtags 

 
## Description 

### starbucks.csv / dunkin.csv 

 Description of columns added/modified 

| Column | Description | 
| ------- | ----------- | 
| `id` | Unique id for each tweet (ex: D1, S1, etc.) | 
| `text` | Cleaned text   | 
| `negative` | Percentage of tweet that is negative. <br><br> Good for analyzing the context & presentation of how sentiment is conveyed. See documentation https://github.com/cjhutto/vaderSentiment#about-the-scoring for more: |
| `neutral` | Percentage of tweet that is neutral | 
| `positive` | Percentage of tweet that is positive | 
| `sentiment_score` | sentiment score from -1 to 1 <br><br> Accounts for VADER rule-based enhancements such as word-order sensitivity for sentiment-laden multi-word phrases, etc. This was done on un-clean data to account for things like !! ?? (: CAPITALS ... emojis, etc.  | 
| `sentiment` | Sentiment values based on threshold  <br><br> **positive** :  `sentiment_score` >= 0.05 <br> **neutral** : (`sentiment_score` > -0.05) and (`sentiment_score` < 0.05) <br> **negative** : `sentiment_score` <= -0.05) |





Compound Score or `sentiment_score` is the one most commonly used for sentiment analysis by most researchers
