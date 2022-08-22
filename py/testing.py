from improved_code import *
from starter_code import *
import timeit

def test_processTweets(list_of_tweets, engine):
    """
    Testing the method process_tweets
    
    :param list of tweets: list of tweets to process
    :param engine: tweets processor to test
    """
    print("*Testing Process Tweets")  
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
    else: print("--Successfully Process Tweets")
    
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
    print("*Testing Process Query")
    engine.process_tweets(list_of_tweets)
    try: engine.process_queries("a & (b | c)")
    except: print("--Failed to run correctly")
    else: print("--Successfully Run")
    test_BadQueries(engine)

    good = 0
    try: engine.process_queries("") == {"op0": ["&", ""]}
    except: print("--Good Query Failed to Process: EmptyString")
    else: good += 1

    try: engine.process_queries("notinanytweets") == {"op0": ["&", "notinanytweets"]}
    except: print("--Good Query Failed to Process: notinanytweets")
    else: good += 1
    
    try: engine.process_queries("a      b") == {"op0": ["&", "a", "b"]}
    except: print("--Good Query  Failed to Process: a      b")
    else: good += 1
    
    try: engine.process_queries("a & b &") == {"op0": ["&", "a", "b"]}
    except: print("--Good Query Failed to Process: a & b &")
    else: good += 1
    
    try: engine.process_queries("!a") == {"op0": ["!", "a"]}
    except: print("--Good Query Failed to Process: !a")
    else: good += 1
    
    try: engine.process_queries("a & !(b | c)") == {"op0": ["|", "b", "c"],
                                                    "op1": ["!", "op0"],
                                                    "op2": ["&", "a", "op1"]}
    except: print("--Good Query Failed to Process: a & !(b | c)")
    else: good += 1

    try: engine.process_queries("a & ( b | !c )") == {"op0": ["!", "c"],
                                                      "op1": ["|", "b", "op0"],
                                                      "op2": ["&", "a", "op1"]}
    except: print("--Good Query Failed to Process: a & ( b | !c )")
    else: good += 1

    if good == 7: print("--Successfully Process Query")

def test_searchTweets(list_of_tweets, base_engine, new_engine):
    """
    Test the method Search

    :param list_of_tweets: list of tweets to process
    :param base_engine: old engine, used to compared results with new_engine
    :param new_engine: new engine, needed to be tested
    """
    print("*Testing Search Query")
    new_engine.process_tweets(list_of_tweets)
    base_engine.process_tweets(list_of_tweets)
    try: new_engine.search("")
    except: print("--Failed to run correctly")
    else: print("--Successfully Run")

    good = 0
    try: new_engine.search("") == []
    except: print("--Failed to Search: EmptyString")
    else: good += 1

    try: new_engine.search("notinanytweets") == []
    except: print("--Failed to Search: notinanytweets")
    else: good += 1
    
    try: len(new_engine.search("Neeva")) == 5
    except: print("--Failed to Search: Neeva")
    else: good += 1
    
    try: 
        new_results = new_engine.search("neeva")
        base_results = base_engine.search("neeva")
        assert new_results[0] == base_results[0][0]
    except: print("--Not Matched Results from Base Engine and New Engine: Neeva")
    else: good += 1

    try: 
        results = new_engine.search("!Neeva")
        for res in results:
            assert "neeva" not in res
    except: print("--Failed to Search: !Neeva")
    else: good += 1
    
    try: 
        results = new_engine.search("hello & !(neeva | is)")
        for res in results:
            assert "hello" in res
            assert "neeva" not in res
            assert "is" not in res 
    except: print("--Failed to Search: hello & !(neeva | is)")
    else: good += 1

    if good == 6: print("--Successfully Search Query")

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
    
def time_Process_Tweets():
    """
    Timing the process_tweets method
    """

    setup_code = """
import improved_code
import starter_code
import testing

base_engine = starter_code.TweetIndex()
new_engine = improved_code.ImprovedTweetIndex() 
list_of_tweets = testing.get_tweetslist("tweets")
                 """

    test_code1 = """base_engine.process_tweets(list_of_tweets)"""
    test_code2 = """new_engine.process_tweets(list_of_tweets)"""

    base_time = timeit.timeit(stmt=test_code1, setup=setup_code, number=1000)
    print(f"--Benchmark Time: {base_time:.10} secs")
    new_time = timeit.timeit(stmt=test_code2, setup=setup_code, number=1000)
    print(f"--New Approach Time: {new_time:.10} secs")

def time_Search():
    """
    Timing the serach method
    """

    setup_code = """
import improved_code
import starter_code
import testing

base_engine = starter_code.TweetIndex()
new_engine = improved_code.ImprovedTweetIndex() 
list_of_tweets = testing.get_tweetslist("tweets")
base_engine.process_tweets(list_of_tweets)
new_engine.process_tweets(list_of_tweets)
                 """

    test_code1 = """base_engine.search("neeva")"""
    test_code2 = """new_engine.search("neeva")"""

    base_time = timeit.timeit(stmt=test_code1, setup=setup_code, number=1000)
    print(f"--Benchmark Time: {base_time:.10} secs")
    new_time = timeit.timeit(stmt=test_code2, setup=setup_code, number=1000)
    print(f"--New Approach Time: {new_time:.10} secs")

if __name__ == "__main__":
    list_of_tweets = get_tweetslist("small")
    base_engine = TweetIndex()
    new_engine = ImprovedTweetIndex() 
    test_processTweets(list_of_tweets, new_engine)
    test_processQueries(list_of_tweets, new_engine)
    test_searchTweets(list_of_tweets, base_engine, new_engine)
    print("*Processing Time (running 1000 times):")
    time_Process_Tweets()
    print("*Searching Time (running 1000 times):")
    time_Search()