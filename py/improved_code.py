import csv
import re
import queue
import json 

def errors(query):
    """Raise Exception"""
    raise Exception(f"Syntax Errors in Query: {query}")

def valid_bracket_struct(struct):
    """
    Return True if all open parentheses have their own close parentheses.
    Otherwise, return False
    """
    # print(struct)
    brackets = {'(': ')'}
    stack = []
    for i in range(len(struct)):
        if struct[i] == "(":
            stack.append(struct[i])
        else:
            if len(stack) == 0 or brackets[stack.pop()] != struct[i]:
                return False
    return False if len(stack) != 0 else True
    
class ImprovedTweetIndex:
    """ An improved search engine"""

    def __init__(self):
        self.__tweeted_words = dict()
        self.__tweeted_time = dict()

    def __process_tweets_helper(self, tweet):
        """
        Given a tweet, save all the tweeted words as key into a 
        dictionary-based __tweeted_words. Each key will associate 
        with a set of tweets that contain the key.
        """

        # for every word in the tweet
        tweet_words = set(tweet.split(" "))
        for word in tweet_words:
            try: self.__tweeted_words[word.lower()]
            # add the word to dict as key, save the tweet under that key
            except: self.__tweeted_words[word.lower()] = {tweet.lower()}
            else: self.__tweeted_words[word.lower()].add(tweet.lower()) 

    def process_tweets(self, list_of_timestamps_and_tweets):
        """
        Given a list of timestamps and tweet, save all tweeted words as key 
        into a dictionary-based __tweeted_words. Each key will associate with 
        a set of tweets that contain the key. 
        
        Make each tweet a key in __tweeted_time, associate with each key is 
        the timestamp of the tweet 

        :param list_of_timestamps_and_tweets: A list of tuples consisting 
        of a timestamp and a tweet.
        """

        for timestamp, tweet in list_of_timestamps_and_tweets:
            try: self.__tweeted_time[tweet.lower()]
            except:
                self.__tweeted_time[tweet.lower()] = timestamp
                self.__process_tweets_helper(tweet)
            else:
                if self.__tweeted_time[tweet.lower()] < timestamp:
                    self.__tweeted_time[tweet.lower()] = timestamp
            
        self.__time_tweeted = {y: x for x, y in self.__tweeted_time.items()}

    def __is_valid_query(self, query):
        """
        If query is Valid, return True if logical operator exist, False otherwise.
        If query is not Valid, raise Exception. 

        :param query: the given query string
        """
        # if logical operators exists
        if not re.search(r'[\&\|\!]', query):
            return False
        # if logical operator exists
        # no: &word or |word or word& or word| or a!b
        if re.search(r'[\&\|]\w+|\w+[\&\|]|\w!\w', query): 
            errors(query)
        # yes: ( ) must exists if both AND and OR operators are found
        if re.search(r'\&', query) and re.search(r'\|', query) \
        and not re.search(r'[\(\)]', query):
            errors(query)
        # no: using multiple query words before logical operator, e.i, a b & c d
        if re.search(r"\w+ (\!\w+|\w+) ([\|\&])", query) \
        or re.search(r"([\|\&]) (\!\w+|\w+) (\!\w+|\w+)", query):
            errors(query)
        # check if the parenthesis system was input correctly
        bracket_str = re.sub(r'[\!\&\|\w\d\s]', "", query)
        if not valid_bracket_struct(bracket_str):
            errors(query)
        return True

    def __process_queries(self, query):
        """
        Return the set of operations found in the query string. 
        Dissect the query string into different operations, 
        prioritize query with NOT operator, then query in parentheses. 
        Suppose query A & (C | D).

        A & operation 0 (for operation 0 = C | D)
        operation 1     (for operation1 = A & operation 0)

        Save each operation as 
            
        {op#: [logical operator, query word1, query word2]}. 

        :param query: the given query string
        """

        query = re.sub(r'\s\s+', ' ', query) # delete unwanted white spaces
        logical_exists = self.__is_valid_query(query)

        # query with no logical operator
        if not logical_exists:
            return {'op0': ['&'] + query.split(" ")}

        operations = {}
        op_num = 0
        instr = None
        while logical_exists:
            try: 
                # process the NOT operator first
                instr = re.search(r'\!\w+', query)
                if instr: operations["op" + str(op_num)] = ['!', instr[0][1:].lower()]

                # process the query in parenthese as soon as possible
                elif re.search(r"[\(\)]", query):
                    instr = re.search(r"(?:\(|\(\s)(\w+) ([\|\&]) (\w+)(?:\)|\s\))", query)
                    operations["op" + str(op_num)] = [instr[2], 
                                                      instr[1].lower(), 
                                                      instr[3].lower()]
                else: # when all parenthese are gone, process left to right
                    instr = re.search(r"(\w+) ([\|\&]) (\w+)", query)
                    operations["op" + str(op_num)] = [instr[2], 
                                                      instr[1].lower(), 
                                                      instr[3].lower()]
                # update query
                query = query.replace(instr[0], "op" + str(op_num))
                op_num += 1
            except:
                break
        return operations

    def __set_operation(self, operator, set1, set2):
        """
        Perform set operation between two sets with given operator
        :param operator: set operator
        :param set1, set2: two sets to use for the operation
        """
        if operator == "!":
            return set1 - set2
        elif operator == "&":
            return set1 & set2
        return set1 | set2

    def __process_query_word(self, query, instructions):
        """
        Return a list of sets of tweets and a set operator. 
        For each query in instructions, match the set of tweets
        that contain the query.

        :param query: query words in the instructions
        :param instructions: another dictionary of query words
        """
        for i in range(1, len(query)):
            if not re.search('op', query[i]):
                try:
                    query[i] = self.__tweeted_words[query[i]]
                except:
                    query[i] = set()
            else:
                query[i] = instructions[query[i]]
        return query


    def __search_helper(self, instructions):
        """
        Return all the tweets that satisfied the conditions in the 
        instructions.

        :param instructions: a dictionary all queries
        """

        all_tweets = set(self.__tweeted_time.keys())
        results = set()
        for stage in instructions:
            log_op = instructions[stage][0]
            working_sets = self.__process_query_word(instructions[stage], 
                                                     instructions)
            # print(working_sets)
            if len(working_sets) <= 2:
                instructions[stage] = self.__set_operation(log_op, all_tweets, working_sets[1])
            else:
                instructions[stage] = self.__set_operation(log_op, working_sets[1], working_sets[2])
        return instructions['op' + str(len(instructions) - 1)]


    def search(self, query):
        """
        Given a query, for each word in the query, find five 
        different tweets with the highest timestamps.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), 
        ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """

        # print(query)
        recent_five = []
        recent_time = []
        instructions = self.__process_queries(query)
        found_tweets = self.__search_helper(instructions)
       


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
    # print(list_of_tweets)
    ti = ImprovedTweetIndex()
    ti.process_tweets(list_of_tweets)
    # ti.search('hello world')
    ti.search('Neeva & search & ((works | stuff) | !(not & world))')
    # ti.search('Neeva & !search & stuffs & great')
    # ti.search('Neeva & !(not | world)')
    # ti.search('Neeva | mine !Google | his Yahoo')
    # ti.search('')