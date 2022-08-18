from improved_code import *
from starter_code import *
import time

def test_processTweets(base_enging, new_engine, list_of_tweets):
    """Testing the method process_tweets"""
    print("--Testing Process Tweets--")
    
    try:
        new_engine.process_tweets(list_of_tweets)
    except:
        print("--Failed to run correctly")
        raise
    else:
        print("--Successfully Run")

    try:
        assert new_engine.tweeted_word_library["hello"][10] == "hello neeva this is neeva"
        assert new_engine.tweeted_word_library["this"][11] != "hello neeva this is neeva"
        assert new_engine.tweeted_word_library["stuff"][12] == "hello stuff"
    except:
        print("--Incorrect Outputs")
        raise
    else:
        print("--All outputs are corrects")
    
    start = time.time()
    for _ in range(1000):
        base_enging.process_tweets(list_of_tweets)
    end = time.time()
    print(f"Base Engine - Processing tweets 1000 times took: {end - start:.10f}")
    
    start = time.time()
    for _ in range(1000):
        base_enging.process_tweets(list_of_tweets)
    end = time.time()
    print(f"New Engine  - Processing tweets 1000 times took: {end - start:.10f}")
    

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
            
    base_ti = TweetIndex()
    new_ti = ImprovedTweetIndex() 
    test_processTweets(base_ti, new_ti, list_of_tweets)
