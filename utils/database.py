from sqlite3 import Connection, connect
from typing import List, Tuple
from utils.constants import TWEETS_DATABASE_NAME, SQL_CREATE_TWEETS_TABLE, SQL_INSERT_TWEET, SQL_SELECT_TWEETS



class Database:
    __conn : Connection

    def create_connection(self, db_file : str) -> None:
        self.__conn = connect(db_file)

    def create_table(self, create_table_sql : str) -> None:
        cur = self.__conn.cursor()
        cur.execute(create_table_sql)

    def insert(self, insert_sql : str, data : tuple) -> None:
        cur = self.__conn.cursor()
        cur.execute(insert_sql, data)
        self.__conn.commit()

    def insert_many(self, insert_sql : str, data_list : List[tuple]) -> None:
        cur = self.__conn.cursor()
        cur.executemany(insert_sql, data_list)
        self.__conn.commit()

    def select(self, select_sql : str) -> list:
        cur = self.__conn.cursor()
        cur.execute(select_sql)
        return cur.fetchall()


class TweetsDatabase:
    def __init__(self):
        self.db = Database()
        self.db.create_connection(TWEETS_DATABASE_NAME)
        self.db.create_table(SQL_CREATE_TWEETS_TABLE)

    def insert_mult_tweets(self, tweets : List[Tuple[str, str]]) -> None:
        self.db.insert_many(SQL_INSERT_TWEET, tweets)

    def insert_tweet(self, tweet : Tuple[str, str]) -> None:
        self.db.insert(SQL_INSERT_TWEET, tweet)

    def get_tweets(self) -> List[Tuple[str, str]]:
        return self.db.select(SQL_SELECT_TWEETS)
