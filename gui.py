from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
from logic import Logic
from utils.database import TweetsDatabase
from utils.sentiment import SentimentAnalysisRawTextblob, SentimentAnalysisNltk, SentimentAnalysisSklearn, SentimentAnalysisTextblob



class GUI:
    root = Tk()

    consumer_key_el : Entry
    consumer_secret_el : Entry
    access_key_el : Entry
    access_secret_el : Entry

    twitter_username_el : Entry
    number_of_tweets_el : Entry
    sentiment_combo : Combobox

    current_user_name_el : Message
    current_user_rating_el : Message
    current_user_tweets_types_el : Message
    tweet_number_combo : Combobox
    current_tweet_el : ScrolledText
    current_tweet_rating_el : Message

    def __init__(self, logic : Logic, database : TweetsDatabase):
        self.logic = logic
        self.database = database
        self.draw_api_keys()
        self.root.title("Sentiment analysis")
        self.root.mainloop()

    def draw_api_keys(self):
        Label(self.root, text="Consumer key").grid(row=0)
        self.consumer_key_el = Entry(self.root, show="*", width=30)
        self.consumer_key_el.grid(row=1, padx=10, pady=10)

        Label(self.root, text="Consumer secret").grid(row=2)
        self.consumer_secret_el = Entry(self.root, show="*", width=30)
        self.consumer_secret_el.grid(row=3, padx=10, pady=10)

        Label(self.root, text="Access key").grid(row=4)
        self.access_key_el = Entry(self.root, show="*", width=30)
        self.access_key_el.grid(row=5, padx=10, pady=10)

        Label(self.root, text="Access secret").grid(row=6)
        self.access_secret_el = Entry(self.root, show="*", width=30)
        self.access_secret_el.grid(row=7, padx=10, pady=10)

        self.__load_keys()

        Button(self.root, text="Ok", command=self.__api_keys_ok_button, padx=10, pady=5).grid(row=8)

    def __load_keys(self):
        keys = self.logic.load_keys()
        self.consumer_key_el.insert(0, keys[0])
        self.consumer_secret_el.insert(0, keys[1])
        self.access_key_el.insert(0, keys[2])
        self.access_secret_el.insert(0, keys[3])

    def __api_keys_ok_button(self):
        keys = [self.consumer_key_el.get(), self.consumer_secret_el.get(), self.access_key_el.get(), self.access_secret_el.get()]
        self.logic.save_keys(keys)
        self.__goToUserSetter()

    def draw_user_setter(self):
        Label(self.root, text="Twitter username").grid(row=0)
        self.twitter_username_el = Entry(self.root, width=30)
        self.twitter_username_el.grid(row=1, padx=10, pady=10)

        Label(self.root, text="Number of tweets").grid(row=2)
        self.number_of_tweets_el = Entry(self.root, width=30)
        self.number_of_tweets_el.grid(row=3, padx=10, pady=10)

        self.sentiment_combo = Combobox(self.root)
        self.sentiment_combo['values'] = ['Sklearn', 'Textblob', 'RawTextblob', 'Nltk']
        self.sentiment_combo.grid(row=4, padx=10, pady=10)
        self.sentiment_combo.bind("<<ComboboxSelected>>", self.__comboStrategyChange)

        Button(self.root, text="Ok", command=self.__user_setter_ok_button, padx=10, pady=5).grid(row=5)

    def __comboStrategyChange(self, event):
        sentiment_strategy = self.sentiment_combo.current()
        if sentiment_strategy == 0:
            self.logic.set_analyser(SentimentAnalysisSklearn())
        elif sentiment_strategy == 1:
            self.logic.set_analyser(SentimentAnalysisTextblob())
        elif sentiment_strategy == 2:
            self.logic.set_analyser(SentimentAnalysisRawTextblob())
        elif sentiment_strategy == 3:
            self.logic.set_analyser(SentimentAnalysisNltk())

    def __user_setter_ok_button(self):
        self.logic.train_analyzer(self.database.get_tweets())
        self.user_data = self.logic.analyze_user(self.twitter_username_el.get(), int(self.number_of_tweets_el.get()))
        self.tweet_count = len(self.user_data[1])

        self.__goToUserAnalysis()

        self.current_user_name_el.configure(text=self.user_data[0])
        self.current_user_rating_el.configure(text=self.user_data[3])
        self.current_user_rating_el.configure(text=self.user_data[3])
        self.current_user_tweets_types_el.configure(text=(str(self.user_data[4][0]) + ' / ' + str(self.user_data[4][2]) + ' / ' + str(self.user_data[4][1])))

    def draw_user_analysis(self):
        Label(self.root, text="User:").grid(row=0, column=0)
        self.current_user_name_el = Message(self.root, width=200)
        self.current_user_name_el.grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="Rating:").grid(row=1, column=0)
        self.current_user_rating_el = Message(self.root, width=200)
        self.current_user_rating_el.grid(row=1, column=1, padx=10, pady=10)

        Label(self.root, text="Pos / Neut / Neg:").grid(row=2, column=0)
        self.current_user_tweets_types_el = Message(self.root, width=200)
        self.current_user_tweets_types_el.grid(row=2, column=1, padx=10, pady=10)

        self.tweet_number_combo = Combobox(self.root)
        values = []
        for i in range(self.tweet_count):
            values.append('Tweet ' + str(i + 1))
        self.tweet_number_combo['values'] = values
        self.tweet_number_combo.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.tweet_number_combo.bind("<<ComboboxSelected>>", self.__comboChange)

        self.current_tweet_el = ScrolledText(self.root, width=40, height=10, wrap="word")
        self.current_tweet_el.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.current_tweet_rating_el = Message(self.root, width=200)
        self.current_tweet_rating_el.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        Button(self.root, text="Back", command=self.__goToUserSetter, padx=10, pady=5).grid(row=6, column=0)
        Button(self.root, text="Save analysis to file..", command=self.__save_analysis_to_file, padx=10, pady=5).grid(row=6, column=1)

    def __comboChange(self, event):
        tweet_number = self.tweet_number_combo.current()
        self.set_current_tweet_content(self.user_data[1][tweet_number])
        self.set_current_tweet_rating(self.user_data[2][tweet_number])

    def set_current_tweet_content(self, tweet_content):
        self.current_tweet_el.delete(1.0, END)
        self.current_tweet_el.insert(INSERT, tweet_content)

    def set_current_tweet_rating(self, tweet_rating):
        self.current_tweet_rating_el.configure(text=tweet_rating)

    def __save_analysis_to_file(self):
        self.logic.save_analysis_to_file(self.user_data[0], self.user_data[3], self.user_data[4])

    def __createNewWindow(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title("Sentiment analysis")

    def __goToApiKeys(self):
        self.__createNewWindow()
        self.draw_api_keys()

    def __goToUserSetter(self):
        self.__createNewWindow()
        self.draw_user_setter()

    def __goToUserAnalysis(self):
        self.__createNewWindow()
        self.draw_user_analysis()
