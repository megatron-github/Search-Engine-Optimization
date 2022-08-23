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
4. Beside the operator **_NOT_**, there is always a space character to seperate a logical operator and a word in query.
5. When logical operator exists, every two words in the query must be seperated by a logical operator.
6. When **_AND_** and **_OR_** operator are included in the query, parentheses must also be included.
7. All parentheses must be included and formatted correctly.
8. A tweet will never have special characters such as **!, &, |**.
9. The returning five most recent tweets are all unique.

### Processing Tweets

To optimize the running time of `search()`, we may want to share the finding job of `search()` with `process_tweets()`. We know that the running time of `search()` is 
```
O(l·m·n) for l = # words in the query, m = # words in the tweet, and n = # available tweets. 
```

With Python's dictionary (similar to a hash table), we can save each word in a tweet as a unique key. Under each key, we will build a set of tweets that contain the keyword (i.e, key = "hello", tweets(key) = {"hello world"}). Using the keyword, we can access the desired set of tweets in *O(1)*-time. With such an approach, we don't have to worry about the number of words in each tweet going forward. Thus, we will have new time complexity of 
```
O(l·n) for l = # words in the query, and n = # available tweets. 
```
We want to store the tweets containing the keyword into a set because we want to perform set operations when filtering for desired tweets.

In addition, we will also build another dictionary with the tweet strings as keys. Associated with each key is the tweet's timestamp. We only want to save the tweet's latest timestamp in case of a tweet is repeated. With this set of data, we will have access to all the tweets and their timestamps given by the users. We need a set of all the tweets to deal with the logical operator **_!_ (_NOT_)** and the set operation Difference.

### Set Operations

Given a search query, we desired a set of tweets, where each tweet in the set contains all of the query words. Now that, for each query word, we can retrieve a set of tweets. Our desired set of tweets is the **Intersection** of all retrieved sets. Since we want to extend our search engine to handle search operations such as **_&_ (_AND_)**, **_|_ (_OR_)**, and **_!_ (_NOT_)**, we want to apply other set operations such as **Union** and **Difference**. 

We use **Intersection** when we want a set of tweets, where each tweet contains all the query words (i.e logical operator **_AND_**). We can apply a similar idea with the operation **Union**. Similar to the logical operator **_OR_**, **Union** returns a set of tweets, where each tweet contains one or more than two query words. With the logical operator **_NOT_**, we want to retrieve all the tweets that do not include the query word. Given *S* = the set of all available tweets, the operation **Difference** will subtract all the tweets containing the query word from *S*. Python has optimized built-in functions for all the mentioned set operations. Given the sets *s* and *t*, the average running time of Python set operations is *O(len(s) or len(t))*. For intersection, the worst case is *O(len(s) · len(t))*. The biggest set of tweets we can retrieve is the set of all available tweets. Thus, on average, we can understand the time complexity of set operations to be 
```
O(n) for n = # available tweets.
```

### Processing Queries

Now that we can get a set of tweets knowing a word inside the desired tweets and perform set operations, we can extend our search engine to handle logical operators such as **_&_ (_AND_)**, **_|_ (_OR_)**, and **_!_ (_NOT_)**. From our **Assumptions**, the standard format for a query with logical operators is 
```
For operators: & and |:
"query_A OPERATOR query_B"

For operator: !
"!query_A".
```
The query string may also include parentheses telling which sets and operations to do first. 

Given a complicated query with multiple set operations, we will need break down the query string into parts and steps. Suppose we have given a query string of 
```
"A & (B | C) & !D".
```
Our approach is to apply the idea of LIFO. First, we will deal with all words preceded by the logical operator **_!_ (_NOT_)** by saving it into a Python dictionary-based instruction set as
```
instruction set:
{
    op0: [!, D]
}

query string updated to:
"A & (B | C) & op0".
```
Then, we process all operations in the parentheses with the updated query string to have
```
instruction set updated to:
{
    op0: [!, D],
    op1: [|, B, C]
}

query string updated to:
"A & op1 & op0".
```
For query strings containing logical operators, we will continue to process and update the query string until all logical operators are gone. After processing all query words preceded by logical operator **_!_ (_NOT_)** and query strings inside parentheses, we will process the query string from left to right, i.e,
```
instruction set updated to:
{
    op0: [!, D],
    op1: [|, B, C],
    op2: [&, A, op1],
    op3: [&, op2, op0]
}

query string updated to:
"A & op1 & op0",
"op2 & op0",
"op3"
```
The number of operation in the instruction set is equal to the number of logical operators found in the input query string. The number of operations in the instruction set equals the number of logical operators in the input query string. For query string without logical operators, we will save the query string as
```
instruction set = { op0: [&, query_word1, query_word2, ...] }
```
For a query string without a logical operator, the number of operations in the instruction set equals the number of query words in the input query string.

The algorithm used for this section utilized Python's regular expression. Thus, the time complexity of this section depends on the length of the query string and string search via regular expression.

### Searching Tweets

To search for a set of recent tweets, the `search()` asks users to give a query string as an argument. Then, it will process the query strings to get the instruction set. For each operation in the instruction set, the search engine will use the query words to find the desired sets of tweets and perform the needed set operation. The set of tweets created from the last instruction will satisfy all the conditions in the query string. The engine will sort the final set of tweets in reverse order using the timestamp of each tweet. Then it returns the first five tweets from the set. 

The time complexity of `search()` depends on the length of the query string, string search via regular expression, the running time of each set operations, and the sorting time of the final set. 
```
Let k = time complexity of processing queries (via regular expression)
Let h = # operations in the instruction set/# query words in the input query string
```
For each instruction, `search()` is expected to perform some set operations with the complexity of 
```
O(n) for n = # available tweets.
```
For each instruction, `search()` is expected to perform some set operations with the complexity of *O(n)*. Thus, the running time of finding the set of tweets that satisfied the query is
```
O(h·n) for  h = # operations in the instruction set, and n = # available tweets.
```
Since the query string is often very small compared to the list of all available tweets, *O(h·n)* will become more of *O(n)* in average as *n* get biggers.
The sorting algorithm is optimized by Python and has the time complexity of 
```
O(n·lgn) for n = # available tweets.
```
Thus, the time complexity of `search()` is
```
O(k) + O(h·n) + O(n·lgn).
```

Even though the time complexity of the newer search engine may look worse than the starter code — **_O(n·lgn)_ vs. _O(l·m·n)_**. However, the term **_n_** in the time complexity of the newer engine does not always equal the entire list of available tweets. On average, the new engine only has to work with a fraction of all available tweets, given that every tweet is a little different from one another. The term **_n_** in the time complexity of the older engine implies all available tweets. As the list of available tweets gets bigger, the query string gets more complicated, or the tweets get longer, the new engine will prevail as the winner. 

## Performance/Report

### Part 1:
```
Evaluating with data: tweets.csv
Search query:         "neeva"
```

Benchmark (given) version:
```
process_tweets (processing 1000 times) took ~2.716411115 secs.
search         (searching 1000 times)  took ~4.227682672 secs.
```

Improved (new) version:
```
process_tweets (processing 1000 times) took ~2.759720021 secs.
search         (searching 1000 times)  took ~3.783080801 secs.
```

### Part 2:

Benchmark (given) version:
```
Evaluating with data: tweets.csv
Search query:         "neeva special way"
process_tweets (processing 1000 times) took ~2.699869635 secs.
search         (searching 1000 times)  took ~5.071821972 secs.
```

Improved (new) version:
```
Evaluating with data: tweets.csv
Search query:         "neeva & special & way"
process_tweets (processing 1000 times) took ~2.773678478 secs.
search         (searching 1000 times)  took ~0.595057001 secs.
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
cd py
python starter_code.py 
```

To run new tweet searching engine
```
cd py
python improved_code.py
```

To see test results and times of the tweet searching engines
```
cd py
python testing.py
```

## Author

Truong Pham
