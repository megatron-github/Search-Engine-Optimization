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
        self.tweeted_words = {}
        self.tweeted_time = {}

    def process_tweets(self, list_of_timestamps_and_tweets):
        """
        Given a list of timestamps and tweet, for each tweet in the list, 
        save all tweeted words as key into a dictionary-based tweeted_words. 
        Each key will associate with a set of tweets that contain the key. 
        
        Make each tweet a key in tweeted_time, associate with each key is 
        the timestamp of the tweet 

        :param list_of_timestamps_and_tweets: A list of tuples consisting 
        of a timestamp and a tweet.
        """

        for timestamp, tweet in list_of_timestamps_and_tweets:
            tweet_words = set(tweet.split(" "))
            # for every word in the tweet
            for word in tweet_words:
                try: self.tweeted_words[word.lower()]
                # add the word to dict as key, save the tweet under that key
                except: self.tweeted_words[word.lower()] = {tweet.lower()}
                else: self.tweeted_words[word.lower()].add(tweet.lower()) 
            # a dictionary with the tweet as key, save the time under that key
            self.tweeted_time[tweet.lower()] = timestamp

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

    def __search_helper(self, instructions):
        """
        Use the set of instructions, find all the tweets that satisfied
        the conditions in the instructions

        :param instructions: a dictionary all queries
        """
        for item in instructions:
            print(instructions[item])

    def search(self, query):
        """
        Given a query, for each word in the query, find five 
        different tweets with the highest timestamps.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), 
        ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        set_a = {(1, 'b'), (2, 'b'), (3, 'b'), (10, 'b'), (9, 'b')}
        set_b = {(3, 'b'), (4, 'b'), (5, 'b'), (6, 'b')}
        diff = set_a ^ set_b
        union = set_a | set_b
        intersection = set_a & set_b

        print(query)
        instructions = self.__process_queries(query)
        found_tweets = self.__search_helper(instructions)
        print()


        # json_obj = json.dumps(instructions, indent=2)
        # print(json_obj)


        # # result = []
        # # for word in query_words:
        # #     word.lower()
        # #     pass
        # # return result



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
    ti.process_tweets(list_of_tweets)
    ti.search('hello world')
    ti.search('Noovi & search & ((works & great) | !(needs & improvement))')
    ti.search('Noovi & search & !works & great')
    ti.search('Noovi & (!great | !fast)')
    # ti.search('Noovi | mine !Google | his Yahoo')
    ti.search('')