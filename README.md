# Neeva_BE
Neeva First Coding Interview - BE Challenge

## Problem Overview

Engineers at Noovi have built their own search engine, and now it's time to add tweets! After building an initial version of their tweet search system, they believe it can be better. Right now, it returns the most recent tweet (highest timestamp) whose tweet text contains all of the words in the query. They Noovi team wants you to help improve it in 3 specific ways:

1. They want searching to be faster on a large set of tweets.
2. They want to return the top 5 most recent tweets instea of a single tweet.
3. They want to be able to handle search operators like logical operators such as `&` (AND), `|` (OR), and `!` (NOT), as well as grouping by parentheses `(` and `)`.

## Background

The search engine object `TweetIndex` had two methods `Search()` and `Process()` to find the most recent tweet. While the method `Process()` stores all the tweets in an array, the method `Search()` goes through the array of tweets to find the most recent tweet that contains all the words in the query. Consider the worst case scenario, the engine will have to go through all the tweets in the array. For each tweet, it needs to check whether the tweet contain all the words in the query. The time complexity of the search operation will get worse with larger sets of available tweets and longer query. 

## Approach

We can optimize the run time of `Search()` by sharing the work of finding tweets containing the words in the query with `Process()`. With data structure such as Python's dictionary, we save tweeted each query word as a key and associate it to an array of tweets that contain the key. With such an approach, a larger sets of available tweets will not affect the run time of `Search()`.


