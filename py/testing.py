from improved_code import *
from starter_code import *
import random
import time

def test_processTweets(list_of_tweets, engine):
    """
    Testing the method process_tweets
    
    :param list of tweets: list of tweets to process
    :param engine: tweets processor to test
    """
    print("--Testing Process Tweets")  
    try: engine.process_tweets(list_of_tweets)
    except: print("--Failed to run correctly")
    else: print("--Successfully Run")
    test = 1
    try:
        for item in engine.tweeted_words:                               # 1
            assert len(engine.tweeted_words[item]) > 0
        test += 1
        assert len(engine.tweeted_words['hello']) == 13                 # 2
        test += 1
        assert engine.tweeted_words['yay'] == {'yay'}                   # 3
        test += 1
        assert engine.tweeted_words['neeva'] == {'neeva',               # 4
                                                 'hello neeva this is neeva', 
                                                 'hello neeva this is bob', 
                                                 'hello this is neeva', 
                                                 'hello this is also neeva', 
                                                 'hello neeva me'}
        test += 1
        assert "" not in engine.tweeted_words                           # 5
        test += 1
        keys = engine.tweeted_times.keys()
        for timestamp, tweet in list_of_tweets:                         # 6                        
            tweet = tweet.lower()                           
            assert tweet in keys
            assert engine.tweeted_times[tweet] >= timestamp
    except: print(f"--Errors in Test {test}")
    else: print("--Process Tweets Successfully")
    
def test_BadQueries(engine):
    """
    Testing whether the improved engine will raise error
    if users input bad queries

    :param engine: the query process to be tested
    """
    bad_query = 0
    try: engine.process_queries("a!")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a!")

    try: engine.process_queries("a !b")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a !b")

    try: engine.process_queries("a &b")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a &b")

    try: engine.process_queries("a|b")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a|b")

    try: engine.process_queries("a & b | c")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a & b | c")

    try: engine.process_queries("a | b)")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a | b)")

    try: engine.process_queries("[a & b")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: [a | b")

    try: engine.process_queries("(!a]")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: (!a]")

    try: engine.process_queries("a b & c")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a b & c")

    try: engine.process_queries("a | !b c")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a | !b c")

    try: engine.process_queries("a && b")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a && b")

    try: engine.process_queries("a | | c")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a | | b")

    try: engine.process_queries("a!b")
    except: pass
    else: 
        bad_query += 1
        print("--Bad Query Not Catched: a!b")
    
    assert bad_query == 0

def test_processQueries(list_of_tweets, engine):
    """
    Testing the method process_queries
    
    :param list of tweets: list of tweets to process
    :param engine: queries processor to test
    """
    print("--Testing Process Query")
    engine.process_tweets(list_of_tweets)
    test_BadQueries(engine)
    
        #     queries = [
#                'hello      bob', 'ab c', '',
#                'Noovi & search & (  (works & great) | (needs & improvement))',
#                'Noovi & is & (interesting | exciting ) & !boring',
#                '(interesting | exciting ) & ! boring',
#                'boring!',
#                'Noovi & is & ( interesting | exciting    )',
#                ]


    # try:
    #     assert new_engine.process_queries('hello  bob') == {"OP0": ["hello", "bob"]}
    #     assert new_engine.tweeted_word_library["this"][11] != "hello neeva this is neeva"
    #     assert new_engine.tweeted_word_library["stuff"][12] == "hello stuff"
    # except:
    #     print("--Incorrect Outputs")
    #     raise
    # else:
    #     print("--All outputs are corrects")


def func_timer(func, param, steroidize=False):
    """
    Return the waiting time after the given function 
    is called

    :param func: the function to run
    :param param: the parameter func needs
    :param steroidize: calls func 1000 times
    :return: a float indicating the seconds the given
    function takes from calling to terminating
    """
    time.sleep(1)
    start = None
    end = None
    if steroidize:
        start = time.time()
        for _ in range(1000):
            func(param)
        end = time.time()
    else:
        start = time.time()
        func(param)
        end = time.time()
    return end - start

def process_time(list_of_tweets, base_engine, new_engine):
    """
    Timing the Process Function

    :param list_of_tweets: list of tweets used to process and search
    :param base_engine: the original tweets processor in starter_code
    :param new_engine: the improved tweets processor in improved_Code
    """
    print("--Processing Time:")
    print(f"{'Size':<11} {'Base Time':<19} {'New Time'}")
    size = 1
    while size < len(list_of_tweets):
        print(f"{size:<10}", end="")
        test_sample = random.sample(list_of_tweets, size)

        base_engine.list_of_tweets = []
        assert(len(base_engine.list_of_tweets) == 0)
        base_time = func_timer(base_engine.process_tweets, test_sample, True)
        print(f"{base_time:<20.10f}", end="")
        
        new_engine.tweeted_time = {}
        new_engine.tweeted_words = {}
        assert(len(new_engine.tweeted_words) == 0)
        assert(len(new_engine.tweeted_time) == 0)
        new_time = func_timer(new_engine.process_tweets, test_sample, True)
        print(f"{new_time:.10f}", end='\n')

        size *= 2
    print()
        
def search_time(list_of_tweets, base_engine, new_engine, query):
    """
    Timing the Search function

    :param list_of_tweets: list of tweets used to process and search
    :param base_engine: the original tweets searcher in starter_code
    :param new_engine: the improved tweets searcher in improved_Code
    """
    print("--Searching Time:")
    print(f"{'Size':<11} {'Base Time':<19} {'New Time'}")
    size = 1
    while size < len(list_of_tweets):
        print(f"{size:<10}", end="")
        test_sample = random.sample(list_of_tweets, size)

        base_engine.list_of_tweets = []
        assert(len(base_engine.list_of_tweets) == 0)
        base_engine.process_tweets(test_sample)
        assert(len(base_engine.list_of_tweets) == size)
        base_time = func_timer(base_engine.search, query, True)
        print(f"{base_time:<20.10f}", end="")

        new_engine.tweeted_time = {}
        new_engine.tweeted_words = {}
        assert(len(new_engine.tweeted_words) == 0)
        assert(len(new_engine.tweeted_time) == 0)
        new_engine.process_tweets(test_sample)
        new_time = func_timer(new_engine.search, query, True)
        print(f"{new_time:.10f}", end='\n')

        size *= 2
    print()

def get_tweetslist(filename):
    """
    Return a list of tweets found from given filename
    """
    tweet_csv_filename = "../data/" + filename + ".csv"
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
    return list_of_tweets

if __name__ == "__main__":
    list_of_tweets = get_tweetslist("small")
    base_ti = TweetIndex()
    new_ti = ImprovedTweetIndex() 
    # test_processTweets(list_of_tweets, new_ti)
    test_processQueries(list_of_tweets, new_ti)
    # test_searchTweets(list_of_tweets, new_ti)

    # list_of_tweets = get_tweetslist("tweets")
    # base_ti = TweetIndex()
    # new_ti = ImprovedTweetIndex() 
    # process_time(list_of_tweets, base_ti, new_ti)
    # search_time(list_of_tweets, base_ti, new_ti, "neeva people")

