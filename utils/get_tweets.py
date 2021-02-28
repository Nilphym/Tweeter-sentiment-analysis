from typing import List
import tweepy



def get_tweets(username : str, number_of_tweets : int, keys : List[str]) -> List[str]:
	auth = tweepy.OAuthHandler(keys[0], keys[1])
	auth.set_access_token(keys[2], keys[3])
	api = tweepy.API(auth)

	tweets = []
	for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(number_of_tweets):
		tweets.append(tweet.text)

	return tweets
