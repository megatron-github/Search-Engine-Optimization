# Neeva First Coding Interview - BE Challenge

## Background

Engineers at Noovi have built their own search engine, and now it's time to add tweets! After building an initial version of their tweet search system, they believe it can be better. Right now, it returns the most recent tweet (highest timestamp) whose tweet text contains all of the words in the query. The Noovi team wants you to help improve it in 3 specific ways:

1. They want searching to be faster on a large set of tweets.
2. They want to return the top 5 most recent tweets instead of a single tweet.
3. They want to be able to handle search operators like logical operators such as **& (AND)**, **| (OR)**, and **! (NOT)**, as well as grouping by parentheses **()**.

## Problem Overview

The search engine`TweetIndex` had two methods — `search()` and `process_tweets()` — to find the most recent tweet. The method  `search()` has a parameter `query` telling which kind of tweets to search. The method `process_tweet()` takes a list of tweets as an argument and stores all the tweets into an array. The search engine saves all the tweets in its memory to revisit and return a query-satisfied tweet. 

To search for the latest tweet that satisfied the query, the method `search()` loops through the entire list of tweets. For each tweet, the engine checks if it contains all the words in the query. The engine only selects the tweet that contains all the query words and has the latest timestamp.

The running time of `search()` is affected by the sizes of the query string, the tweet string, and the list of tweets. Thus, the running time of `search()` is 
```
O(l·m·n) for l = # words in the query,  m = # words in the tweet, and n = # available tweets.
```
Hence, as the list of tweets, the length of each tweet strings, and/or the length of the query string gets bigger, the running time of `search()` will get worse and worse.

## Approach

### Assumptions

1. We assume that tweet timestamps are globally unique positive integers.
2. Every two words in a tweets are seperated by a space character.
3. There are no special characters beside 26 letters in the English alphabet and the space character in the tweets.
4. Beside the operator **! (NOT)**, there is always a space character to seperate a logical operator and a word in query.
5. When logical operator exists, every two words in the query must be seperated by a logical operator.
6. When AND and OR operator are included in the query, parentheses must also be included.
7. All parentheses must be included and formatted correctly.
8. A tweet will never have special characters such as **!, &, |**.
9. The returning five most recent tweets are all unique.

### Processing Tweets

To optimize the running time of `search()`, we may want to share the finding job of `search()` with `process_tweets()`. We know that the running time of `search()` is 
```
O(l·m·n) for l = # words in the query, m = # words in the tweet, and n = # available tweets. 
```

With Python's dictionary (similar to a hash table), we can save each word in a tweet as a unique key. Under each key, we will build a set of tweets that contain the keyword (i.e, key = "hello", tweets(key) = {"hello world"}). Using the keyword, we can access the desired set of tweets in *O(1)* time. With such an approach, we don't have to worry about the number of words in each tweet going forward. Thus, we will have new time complexity of 
```
O(l·n) for l = # words in the query, and n = # available tweets. 
```
We want to store the tweets containing the keyword into a set because we want to perform set operations when filtering for desired tweets.

In addition, we will also build another dictionary with the tweet strings as keys. Associated with each key is the tweet's timestamp. We only want to save the tweet's latest timestamp in case of a tweet is repeated. With this set of data, we will have access to all the tweets and their timestamps given by the users. We need a set of all the tweets to deal with the logical operator *! (NOT)* and the set operation Difference.

### Set Operations

Given a search query, we desired a set of tweets, where each tweet in the set contains all of the query words. Now that, for each query word, we can retrieve a set of tweets. Our desired set of tweets is the Intersection of all retrieved sets. Since we want to extend our machine to handle search operations such as **& (AND)**, **| (OR)**, and **! (NOT)**, we want to apply other set operations such as Union and Difference. 

We use Intersection when we want a set of tweets, where each tweet contains all the query words. We can apply a similar idea with the operation Union. Similar to the logical operator OR, Union returns a set of tweets, where each tweet contains one or more than two query words. With the logical operator NOT, we want to retrieve all the tweets that do not include the query word. Given S = the set of all available tweets, the operation Difference will subtract all the tweets containing the query word from S. Python has optimized built-in functions for all the mentioned set operations. Given the sets *s* and *t*, the average running time of Python set operations is *O(len(s) or len(t))*. For intersection, the worst case is *O(len(s) · len(t))*. The biggest set of tweets we can retrieve is the set of all available tweets. Thus, on average, we can understand the time complexity of set operations to be 
```
O(n) for n = # available tweets.
```

### Processing Queries

Now that we can get a set of tweets knowing a word inside the desired tweets and perform set operations, we can extend our machine to handle logical operators such as **& (AND)**, **| (OR)**, and **! (NOT)**. From our **Assumptions**, the standard format for a query with logical operators is 
```
"query_A OPERATOR query_B".
```


### Searching Tweets


## Performance/Report

```
Evaluating with data: tweets.csv
Search query:         "neeva"
```

Benchmark (given) version:
```
process_tweets (running 1000 times) took ~2.716411115 secs.
search         (running 1000 times) took ~4.227682672 secs.
```

Improved (new) version:
```
process_tweets (running 1000 times) took ~2.759720021 secs.
search         (running 1000 times) took ~3.783080801 secs.
```

## How to run

Imported libraries used for the entire projects
```
csv     <!--to open tweets.csv-->
re      <!--to use regular expression for string matching in new engine-->
timeit  <!--to report real running time of the process_tweets() and search() method-->
```

To run old tweet searching engine
```
python starter_code.py
```

To run new tweet searching engine
```
python improved_code.py
```

To test and time the tweet searching engines
```
python testing.py
```

## Author

Truong Pham
