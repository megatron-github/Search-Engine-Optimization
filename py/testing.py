from improved_code import *
from starter_code import *
import time

# def test_processTweets(base_enging, new_engine, list_of_tweets):
#     """Testing the method process_tweets"""
#     print("--Testing Process Tweets")
    
#     try:
#         new_engine.process_tweets(list_of_tweets)
#     except:
#         print("--Failed to run correctly")
#         raise
#     else:
#         print("--Successfully Run")

#     try:
#         assert new_engine.tweeted_word_library["hello"][10] == "hello neeva this is neeva"
#         assert new_engine.tweeted_word_library["this"][11] != "hello neeva this is neeva"
#         assert new_engine.tweeted_word_library["stuff"][12] == "hello stuff"
#     except:
#         print("--Incorrect Outputs")
#         raise
#     else:
#         print("--All outputs are corrects")
    
# def test_processQuery(new_engine):
#     """Testing the method process_tweets"""
#     print("--Testing Process Query")
#     queries = [
#                'hello      bob', 'ab c', '', 
#                 # "hi !hello",
#                 # 'Noovi & rocks', 
#                 # 'Noovi &rocks', 
#                 # 'Noovi|rocks', 
#                 # 'a!b'
#                'Noovi & search & (  (works & great) | (needs & improvement))',
#                'Noovi & is & (interesting | exciting ) & !boring',
#                '(interesting | exciting ) & ! boring',
#                'boring!',
#                'Noovi & is & ( interesting | exciting    )', 
#             #    'Noovi & is & fast | quick'
#                ]
    
#     try:
#         for q in queries:
#             new_engine.process_queries(q)
#     except:
#         print("--Failed to run correctly")
#         raise
#     else:
#         print("--Successfully Run")

    # try:
    #     assert new_engine.process_queries('hello  bob') == {"OP0": ["hello", "bob"]}
    #     assert new_engine.tweeted_word_library["this"][11] != "hello neeva this is neeva"
    #     assert new_engine.tweeted_word_library["stuff"][12] == "hello stuff"
    # except:
    #     print("--Incorrect Outputs")
    #     raise
    # else:
    #     print("--All outputs are corrects")

def process_time(base_enging, new_enging):
    print("--Processing Time:")
    start = time.time()
    for _ in range(1000):
        base_enging.process_tweets(list_of_tweets)
    end = time.time()
    print(f"--Base Engine - Processing tweets 1000 times took: {end - start:.10f}")
    
    start = time.time()
    for _ in range(1000):
        new_enging.process_tweets(list_of_tweets)
    end = time.time()
    print(f"--New Engine  - Processing tweets 1000 times took: {end - start:.10f}")
    
def search_time(base_enging, new_enging):
    print("--Seaching Time:")
    start = time.time()
    for _ in range(100):
        base_enging.search("Neeva & (people | work)")
    end = time.time()
    print(f"--Base Engine - Searching tweets 1000 times took: {end - start:.10f}")
    
    start = time.time()
    for _ in range(100):
        new_enging.search("Neeva & (people | work)")
    end = time.time()
    print(f"--New Engine  - Searching tweets 1000 times took: {end - start:.10f}")
    

if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/tweets.csv"
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
    base_ti.process_tweets(list_of_tweets)
    new_ti.process_tweets(list_of_tweets)
    # process_time(base_ti, new_ti)
    # search_time(base_ti, new_ti)
    base_res = base_ti.search("Neeva your we")
    new_res = new_ti.search("your Neeva we")

    print(base_res)
    print(new_res)
    # assert(base_res[0][0] == new_res[0])

    # new_ti.process_tweets(list_of_tweets)
    # base_ti.process_tweets(list_of_tweets)

    # ti.search("Neeva people")

    # test_processTweets(base_ti, new_ti, list_of_tweets)
    # test_processQuery(new_ti)

