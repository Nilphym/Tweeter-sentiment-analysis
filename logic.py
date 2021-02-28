from os import path
from typing import List, Tuple
from utils.constants import CONF_FILE_NAME, NEGATIVE_TWEET_FLAG, POSITIVE_TWEET_FLAG, POSITIVE_USER_FLAG, \
    NEUTRAL_USER_FLAG, NEGATIVE_USER_FLAG
from utils.get_tweets import get_tweets
from utils.sentiment import SentimentAnalysis



class Logic:
    api_keys : List[str]
    analyzer : SentimentAnalysis

    def set_analyser(self, analyzer : SentimentAnalysis):
        self.analyzer = analyzer

    def save_keys(self, keys : List[str]) -> None:
        self.api_keys = keys
        with open(CONF_FILE_NAME, 'w') as f:
            for i in range(len(keys)):
                f.write(keys[i])
                if i != 3:
                    f.write('\n')

    def load_keys(self) -> List[str]:
        if path.isfile(CONF_FILE_NAME):
            with open(CONF_FILE_NAME, 'r') as f:
                keys = f.read().split('\n')
                if len(keys) == 4:
                    return keys
        return ['', '', '', '']

    def train_analyzer(self, train_tweets : List[Tuple[str, str]]) -> None:
        self.analyzer.train(train_tweets)

    def analyze_user(self, username : str, number_of_tweets : int) -> Tuple[str, List[str], List[str], str, Tuple[int, int, int]]:
        tweets = self.__send_request(username, number_of_tweets)
        tweets_rating = self.__analyze_tweets(tweets)
        user_rating, tweets_types_count = self.__rate_user(tweets_rating)
        return username, tweets, tweets_rating, user_rating, tweets_types_count

    def __send_request(self, username : str, number_of_tweets : int) -> List[str]:
        return get_tweets(username, number_of_tweets, self.api_keys)

    def __analyze_tweets(self, tweets : List[str]) -> List[str]:
        tweets_rating = []
        for tweet in tweets:
            tweets_rating.append((self.analyzer.classify_tweet(tweet)))
        return tweets_rating

    def __rate_user(self, analyzed_tweets : List[str]) -> Tuple[str, Tuple[int, int, int]]:
        pos, neg, neut = 0, 0, 0
        for analyzed_tweet in analyzed_tweets:
            if analyzed_tweet == NEGATIVE_TWEET_FLAG:
                neg += 1
            elif analyzed_tweet == POSITIVE_TWEET_FLAG:
                pos += 1
            else:
                neut += 1

        if pos > neg:
            return POSITIVE_USER_FLAG, (pos, neg, neut)
        if pos == neg:
            return NEUTRAL_USER_FLAG, (pos, neg, neut)
        return NEGATIVE_USER_FLAG, (pos, neg, neut)

    def save_analysis_to_file(self, username : str, user_rating : str, tweets_types_count : Tuple[int, int, int]) -> None:
        filename = username + '_rating.txt'
        with open(filename, 'w') as f:
            f.write(username + '\n')
            f.write('Overall: ' + user_rating + '\n')
            f.write('Pos / Neg / Neut: ' + str(tweets_types_count[0]) + ' / ' + str(tweets_types_count[1]) + ' / ' + str(tweets_types_count[2]))
