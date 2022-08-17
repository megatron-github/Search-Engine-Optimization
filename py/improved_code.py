import csv
import json 

from typing import List, Tuple



class ImprovedTweetIndex:
    """ An improved search engine"""

    def __init__(self):
        self.tweeted_word_library = {}
        self.words_set = set()

    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
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
                if word in self.tweeted_word_library:
                    self.tweeted_word_library[word][timestamp] = tweet
                else:
                    self.tweeted_word_library[word] = {timestamp: tweet}

        json_object = json.dumps(self.tweeted_word_library, indent=2)
        print(json_object)

    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        Given a query, for each word in the query, find five different tweets with the highest 
        timestamps.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest 
        timestamp tweets first. If no such tweet exists, returns empty list.
        """
        query_words = set(query.split(" "))
        result = []
        for words in query_words:
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
    # print(ti.list_of_tweets)
    # assert ti.search("hello") == [('hello this is also neeva', 15)]
    # assert ti.search("hello me") == [('hello not me', 14)]
    # assert ti.search("hello bye") == [('hello bye', 3)]
    # assert ti.search("hello this bob") == [('hello neeva this is bob', 11)]
    # assert ti.search("notinanytweets") == []
    # print("Success!")