import csv
import re
import queue
import json 

class ImprovedTweetIndex:
    """ An improved search engine"""

    def __init__(self):
        self.tweeted_word_library = {}
        self.words_set = set()

    def process_tweets(self, list_of_timestamps_and_tweets):
        """
        Given a list of timestamps and tweet, for each tweet in the list, save all tweeted 
        words as key into a dictionary-based data structure. Each key will associate with a 
        of tweets that contain the key. 

        :param list_of_timestamps_and_tweets: A list of tuples consisting of a timestamp 
        and a tweet.
        """
        for timestamp, tweet in list_of_timestamps_and_tweets:
            tweet_words = set(tweet.split(" "))
            for word in tweet_words:
                try: self.tweeted_word_library[word.lower()]
                except: self.tweeted_word_library[word.lower()] = {int(timestamp): tweet.lower()}
                else: self.tweeted_word_library[word.lower()][int(timestamp)] = tweet.lower() 

    def is_valid_query(self, query):
        """
        Return True is query is Valid. Otherwise, False. 

        :param query: the given query string
        """
        
        "\w\! -> to find any word with a following !"

        "[\(\)] -> to find whether there is parenthesis"

        # check if the parenthesis system was input correctly
        bracket_str = query.replace(r'[\!\&\|\w\d]', "")

        # check if parentheses are included when AND and OR are found

        # check if there exists a word followed by !


    def process_queries(self, query):
        """
        Return a tuple consist of a queue (FIFO) containing instructional 
        strings on what kind of tweets should be searched and a dictionary to
        translate the instructional strings

        :param query: the given query string

        \((\!\w+|\w+) [\|\&] (\!\w+|\w+)\) -> to get anything between ()

        (\!\w+|\w+) [\|\&] (\!\w+|\w+) -> to get "something OPERATORS something"

        \w+\! -> to find any word with a following !

        [\(\)] -> to find whether there is parenthesis

        """
        instruction_q = queue.Queue()

        pass


    def search(self, query):
        """
        Given a query, for each word in the query, find five 
        different tweets with the highest timestamps.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), 
        ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        query_words
        query_words = set(query.split(" "))

        result = []
        for word in query_words:
            word.lower()
            pass
        return result



if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/small.csv"
    list_of_tweets = []
    with open(tweet_csv_filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i == 0:
                # header
                continue
            timestamp = int(row[0])
            tweet = str(row[1])
            list_of_tweets.append((timestamp, tweet))
            
    ti = ImprovedTweetIndex()
    ti.process_tweets(list_of_tweets)