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
        self.instructions = {}

    def process_tweets(self, list_of_timestamps_and_tweets):
        """
        Given a list of timestamps and tweet, for each tweet in the list, 
        save all tweeted words as key into a dictionary-based data structure. 
        Each key will associate with a set of tweets that contain the key. 

        :param list_of_timestamps_and_tweets: A list of tuples consisting 
        of a timestamp and a tweet.
        """

        for timestamp, tweet in list_of_timestamps_and_tweets:
            tweet_words = set(tweet.split(" "))
            for word in tweet_words:
                try: self.tweeted_words[word.lower()]
                except: self.tweeted_words[word.lower()] = {tweet.lower()}
                else: self.tweeted_words[word.lower()].add(tweet.lower()) 
            self.tweeted_time[tweet.lower()] = timestamp

    def is_valid_query(self, query):
        """
        If query is Valid, return True if logical operator exist, False otherwise.
        If query is not Valid, raise Exception. 

        :param query: the given query string
        """
        logical_exists = True
        # if logical operators exists
        if re.search(r'[\&\|]', query):
            # no: &word or |word or word& or word| or a!b
            if re.search(r'[\&\|]\w+|\w+[\&\|]|\w!\w', query): 
                errors(query)
            # yes: ( ) must exists
            if not re.search(r'[\(\)]', query):
                errors(query)
            # check if the parenthesis system was input correctly
            bracket_str = re.sub(r'[\!\&\|\w\d\s]', "", query)
            if not valid_bracket_struct(bracket_str):
                errors(query)
        else:
            logical_exists = False
            # no: !word
            if re.search(r'\!\w+', query):
                errors(query)
        return logical_exists

    def process_queries(self, query):
        """
        Return a tuple consist of a queue (FIFO) containing instructional 
        strings on what kind of tweets should be searched and a dictionary to
        translate the instructional strings

        :param query: the given query string
        """

        query = re.sub(r'\s\s+', ' ', query) # delete unwanted white spaces
        logical_exists = self.is_valid_query(query)

        if not logical_exists:
            self.instructions = {'op0': [None] + query.split(" ")}
            return

        operation = 0
        while True:
            try: 
                if re.search(r"[\(\)]", query):
                    instr = re.search(r"(?:\(|\(\s)(\!\w+|\w+) ([\|\&]) (\!\w+|\w+)(?:\)|\s\))", query)
                else:
                    instr = re.search(r"(\!\w+|\w+) ([\|\&]) (\!\w+|\w+)", query)
                self.instructions["op" + str(operation)] = [instr[2], instr[1].lower(), instr[3].lower()]
                query = query.replace(instr[0], "op" + str(operation))
                operation += 1
            except:
                break
        return

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


        # instr = re.search(r"(?:\(|\(\s)(\!\w+|\w+) ([\|\&]) (\!\w+|\w+)(?:\)|\s\))", query)
        # print(instr.groups())
        # print(instr[0])
        # self.process_queries(query)
        # print(self.tweeted_word_library)
        print(query)
        self.process_queries(query)
        json_obj = json.dumps(self.instructions, indent=2)
        print(json_obj)


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
    ti.search('Noovi & search & ((works & great) | (needs & improvement))')
    # ti.search('')