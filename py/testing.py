import improved_code

def test_processTweets(engine, list_of_tweets):
    """Testing the method process_tweets"""
    Print("----------------------Testing Process Tweets-------------------------")
    
    Print("Success")

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
    test_processTweets(ti, list_of_tweets)
