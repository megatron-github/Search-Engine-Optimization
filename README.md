# Neeva First Coding Interview - BE Challenge

## Problem Overview

Engineers at Noovi have built their own search engine, and now it's time to add tweets! After building an initial version of their tweet search system, they believe it can be better. Right now, it returns the most recent tweet (highest timestamp) whose tweet text contains all of the words in the query. The Noovi team wants you to help improve it in 3 specific ways:

1. They want searching to be faster on a large set of tweets.
2. They want to return the top 5 most recent tweets instead of a single tweet.
3. They want to be able to handle search operators like logical operators such as `& (AND)`, `| (OR)`, and `! (NOT)`, as well as grouping by parentheses `()`.

## Background

The search engine`TweetIndex` had two methods — `search()` and `process_tweets()` — to find the most recent tweet. The method  `search()` has a parameter `query` telling which kind of tweets to search. Thus, the search engine saves all the tweets in its memory to revisit and return a query-satisfied tweet. The engine stores all the tweets in memory using `process_tweets()`. The method `process_tweet()` takes a list of tweets as an argument.

To search for the latest tweet that satisfied the query, the method `search()` must loops through the entire list of tweets. For each tweet, the engine checks if it contains all the words in the query. The engine only selects the tweet that contains all the query words and has the latest timestamp.

The running time of `search()` is affected by the sizes of the query string, the tweet string, and the list of tweets. For `l = number of words in the query`,  `m = number of words in the tweet`, and `n = number of available tweets`, the running time of `search()` is `O(l·m·n)`. Thus, the time complexity of `search()` will get worse and worse with bigger lists of tweets and longer query/tweet strings. 

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

To optimize the running time of `search()`, we may want to share the finding job of `search()` with `process_tweets()`. We know that the running time of `search()` is `O(l·m·n)` for `l = number of words in the query`, `m = number of words in the tweet`, and `n = number of available tweets`. 

With Python's dictionary (similar to a hash table), we can save each word in a tweet as a unique key. Under each key, we will build a set of tweets that contain the keyword. Given the keyword in the query, we can retrieve the desired set of tweets in `O(1)` time. With such an approach, we don't have to worry about the number of words in each tweet going forward. Thus, we will have new time complexity of `O(l·n)` for `l = number of words in the query`, and `n = number of available tweets`. We want to store the tweets containing the keyword into a set because we want to perform set operations when filtering for desired tweets. 

In addition, we will also build another dictionary with the tweet strings as keys. Associated with each key is the tweet's timestamp. We only want to save the tweet's latest timestamp in case of a tweet is repeated. With this set of data, we will have access to all the tweets and their timestamps given by the users. We need a set of all the tweets to deal with the logical operator NOT and the set operation Difference.

### Processing Queries

A query can be a string with only words a

### Searching Tweets


## Performance/Report

Evaluating with data: "tweets.csv"
Search query : "neeva"

Benchmark (given) version:

`
process_tweets (running 1000 times) took ~2.716411115 secs.
search         (running 1000 times) took ~4.227682672 secs.
`

Improved (new) version:

`
process_tweets (running 1000 times) took ~2.759720021 secs.
search         (running 1000 times) took ~3.783080801 secs.
`

## How to run

Imported libraries used for the entire projects

`
csv <!--to open tweets.csv-->
re  <!--to use regular expression for string matching in new engine-->
timeit <!--to report real running time of the process_tweets() and search() method-->
`

To run old tweet searching engine

`
python starter_code.py
`

To run new tweet searching engine

`
python improved_code.py
`

To test and time the tweet searching engines

`
python testing.py
`

## Author

Truong Pham
