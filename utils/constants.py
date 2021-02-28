CONF_FILE_NAME = 'conf.txt'
TWEETS_DATABASE_NAME = 'tweets.db'

POSITIVE_TWEET_FLAG = POSITIVE_USER_FLAG = 'positive'
NEGATIVE_TWEET_FLAG = NEGATIVE_USER_FLAG = 'negative'
NEUTRAL_USER_FLAG = 'neutral'

SQL_CREATE_TWEETS_TABLE = """ CREATE TABLE IF NOT EXISTS Tweets ( id integer PRIMARY KEY, tweet text NOT NULL, sentiment text NOT NULL ) """
SQL_INSERT_TWEET = """ INSERT INTO Tweets(tweet,sentiment) VALUES(?,?) """
SQL_SELECT_TWEETS = """ SELECT tweet, sentiment FROM Tweets"""
