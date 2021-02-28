from abc import ABC, abstractmethod
from typing import KeysView, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer



class SentimentAnalysis(ABC):
    @abstractmethod
    def train(self, tweets : List[Tuple[str, str]]) -> None:
        pass

    @abstractmethod
    def classify_tweet(self, tweet : str) -> str:
        pass

class SentimentAnalysisSklearn(SentimentAnalysis):
    vectorizer : TfidfVectorizer
    tweets_list, tweets_rates = [], []

    def train(self, tweets: List[Tuple[str, str]]) -> None:
        for tweet in tweets:
            self.tweets_list.append(tweet[0])
            self.tweets_rates.append(tweet[1])

    def classify_tweet(self, tweet: str) -> str:
        print("Hello from sklearn")
        self.tweets_list[-1] = tweet
        return self.__classify()

    def __classify(self):
        self.vectorizer = TfidfVectorizer(max_features=2000, min_df=2, max_df=0.8,
                                          stop_words=stopwords.words('english'))
        processed_features = self.vectorizer.fit_transform(self.tweets_list).toarray()
        X_train, X_test, y_train, y_test = train_test_split(processed_features, self.tweets_rates, test_size=0.1, shuffle=False)
        self.text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
        self.text_classifier.fit(X_train, y_train)

        predictions = self.text_classifier.predict(X_test)

        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
        print(accuracy_score(y_test, predictions))

        return predictions[-1]


class SentimentAnalysisTextblob(SentimentAnalysis):
    cl : NaiveBayesClassifier

    def train(self, tweets: List[Tuple[str, str]]) -> None:
        self.cl = NaiveBayesClassifier(tweets)

    def classify_tweet(self, tweet: str) -> str:
        print("Hello from textblob")
        return self.cl.classify(tweet)


class SentimentAnalysisRawTextblob(SentimentAnalysis):
    def train(self, tweets: List[Tuple[str, str]]) -> None:
        return

    def classify_tweet(self, tweet: str) -> str:
        print("Hello from raw textblob")
        tweet_rating = TextBlob(tweet).polarity
        if tweet_rating < 0:
            return 'negative'
        if tweet_rating > 0:
            return 'positive'
        return 'neutral'


class SentimentAnalysisNltk(SentimentAnalysis):
    __classifier : nltk.NaiveBayesClassifier
    __word_features : KeysView

    def train(self, tweets):
        tweets = self.__filter_tweets(tweets)
        self.__word_features = self.__get_word_features(self.__get_words_in_tweets(tweets))
        training_set = nltk.classify.apply_features(self.__extract_features, tweets)
        self.__classifier = nltk.NaiveBayesClassifier.train(training_set)

    def __filter_tweets(self, tweets):
        tweets_filtered = []
        for (words, sentiment) in tweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
            tweets_filtered.append((words_filtered, sentiment))
        return tweets_filtered

    def __get_word_features(self, wordlist):
        wordlist = nltk.FreqDist(wordlist)
        word_features = wordlist.keys()
        return word_features

    def __get_words_in_tweets(self, tweets):
        all_words = []
        for (words, sentiment) in tweets:
            all_words.extend(words)
        return all_words

    def __extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.__word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def classify_tweet(self, tweet):
        print("Hello from nltk")
        return self.__classifier.classify(self.__extract_features(tweet.split()))
