# Neeva First Coding Interview - BE Challenge

## Problem Overview

Engineers at Noovi have built their own search engine, and now it's time to add tweets! After building an initial version of their tweet search system, they believe it can be better. Right now, it returns the most recent tweet (highest timestamp) whose tweet text contains all of the words in the query. The Noovi team wants you to help improve it in 3 specific ways:

1. They want searching to be faster on a large set of tweets.
2. They want to return the top 5 most recent tweets instead of a single tweet.
3. They want to be able to handle search operators like logical operators such as `& (AND)`, `| (OR)`, and `! (NOT)`, as well as grouping by parentheses `()`.

## Background

The search engine`TweetIndex` had two methods — `search()` and `process_tweets()` — to find the most recent tweet. The method  `search()` has a parameter `query` telling which kind of tweets to search. Thus, the search engine saves all the tweets in its memory to revisit and return a query-satisfied tweet. The engine stores all the tweets in memory using `process_tweets()`. The method `process_tweet()` takes a list of tweets as an argument.

To search for the latest tweet that satisfied the query, the method `search()` must loops through the entire list of tweets. For each tweet, the engine checks if it contains all the words in the query. The engine only selects the tweet that contains all the query words and has the latest timestamp.

The running time of `search()` is affected by the sizes of the query string, the tweet string, and the list of tweets. For l = number of words in the query,  m = number of words in the tweet, and n = number of available tweets, the running time of `search()` is O(l·m·n). Thus, the time complexity of `search()` will get worse and worse with bigger lists of tweets and longer query/tweet strings. 

## Approach

### Assumptions

1. We assume that tweet timestamps are globally unique positive integers.
2. Every two words in a tweets are seperated by a space character.
3. There are no special characters beside 26 letters in the English alphabet and the space character in the tweets.
4. Beside the NOT operator `!`, there is always a space character to seperate a logical operator and a word in query.
5. When logical operator exists, every two words in the query must be seperated by a logical operator.
6. When AND and OR operator are included in the query, parentheses must also be included.
7. All parentheses must be included and formatted correctly.
8. A tweet will never have logical operators !, &, |.

### Processing Tweets

To optimize the running time of `search()`, we may want to share the finding job of `search()` with `process_tweets()`. We know that the running time of `search()` is 

`O(l·m·n)` 

for 

`l = number of words in the query`,  
`m = number of words in the tweet`, and 
`n = number of available tweets`. 

With Python's dictionary (similar to a hash table),  we can save each word in a tweet as a unique key. Under each key, we will build a set of tweets that contain the keyword. Given that we know the keyword, the time complexity to access the set of tweets is constant. With such an approach, we don't have to worry about the number of words in each tweet going forward. Our time complexity will be O(ln).

We can optimize the run time of `search()` by sharing the work of finding tweets containing the words in the query with `process_tweets()`. With data structure such as Python's dictionary, we save tweeted each query word as a key and associate it to a set of tweets that contain the key. With such an approach, a larger sets of available tweets will not affect the run time of `search()`.

We also need an optimized data structure to store the set of tweets associated with each words in our tweets-and-words bank (built in the first step). We can optimize space complexity by only saving five tweets that contains the key and has the highest timestamp for each word. For each new tweet, we sort the set of founded tweets with the new tweets by timestamps and select the most recent five. The sorting time has a constant upper bound because the set will have at most six elements at anytime. However, such an approach will cause us problems when handling query with logical operators. Tweets with highest timestamps might not include all the words in the queries with logical operators. 

Python's dictionary can sort the tweets by timestamps in constant time. However, we will have to sarifice space complexity to have an easier time handling queries with logical operators. 

### Processing Queries

A query can be a string with only words a

### Searching Tweets


## Performance

Evaluating data: small.csv

Default version:
``
New Approach version:
``

## How to run

`
python tester.py
`

## Author

Truong
