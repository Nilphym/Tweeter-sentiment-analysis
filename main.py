from csv import reader
from os import path
from gui import GUI
from utils.constants import TWEETS_DATABASE_NAME
from utils.database import TweetsDatabase
from logic import Logic



def insert_to_db_from_csv(file):
    with open(file, encoding="latin-1") as csvfile:
        spamreader = reader(csvfile)
        tweets = []
        for row in spamreader:
            if row[0] == '4':
                sentiment = 'positive'
            elif row[0] == '2':
                sentiment = 'neutral'
            else:
                sentiment = 'negative'
            tweet = row[5]
            tweets.append((tweet, sentiment))
        db = TweetsDatabase()
        db.insert_mult_tweets(tweets)

if __name__ == "__main__":
    logic = Logic()
    database = TweetsDatabase()
    if not path.isfile(TWEETS_DATABASE_NAME):
        insert_to_db_from_csv('testdata.manual.2009.06.14.csv')

    gui = GUI(logic, database)
