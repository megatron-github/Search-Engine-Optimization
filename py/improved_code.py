import csv
from typing import List, Tuple


class ImprovedTweetIndex:
    """ An improved search engine"""

    def __init__(self):
        self.tweeted_word_library = {}
        self.words_set = set()

    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
        
        pass

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
            
    ti = TweetIndex()
    ti.process_tweets(list_of_tweets)
    print(ti.list_of_tweets)
    assert ti.search("hello") == [('hello this is also neeva', 15)]
    assert ti.search("hello me") == [('hello not me', 14)]
    assert ti.search("hello bye") == [('hello bye', 3)]
    assert ti.search("hello this bob") == [('hello neeva this is bob', 11)]
    assert ti.search("notinanytweets") == []
    print("Success!")