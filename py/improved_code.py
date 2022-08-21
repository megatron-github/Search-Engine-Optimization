import csv
import re

def errors(query):
    """Raise Exception"""
    raise Exception(f"Syntax Errors in Query: {query}")

def valid_bracket_struct(struct):
    """
    Return True if all open parentheses have their own close parentheses.
    Otherwise, return False
    """
    brackets = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for i in range(len(struct)):
        if struct[i] in "([{":
            stack.append(struct[i])
        else:
            if len(stack) == 0 or brackets[stack.pop()] != struct[i]:
                return False
    return False if len(stack) != 0 else True
    
class ImprovedTweetIndex:
    """ An improved search engine"""
    def __init__(self):
        self.tweeted_words = dict()
        self.tweeted_times = dict()

    def __process_tweets_helper(self, tweet):
        """
        Given a tweet, save all the tweeted words as key into a 
        dictionary-based tweeted_words. Each key will associate 
        with a set of tweets that contain the key.
        """
        # for every word in the tweet
        tweet_words = set(tweet.split(" "))
        for word in tweet_words:
            try: self.tweeted_words[word]
            # add the word to dict as key, save the tweet under that key
            except: self.tweeted_words[word] = {tweet}
            else: self.tweeted_words[word].add(tweet) 

    def process_tweets(self, list_of_timestamps_and_tweets):
        """
        Given a list of timestamps and tweet, save all tweeted words as key 
        into a dictionary-based tweeted_words. Each key will associate with 
        a set of tweets that contain the key. 
        
        Make each tweet a key in tweeted_times, associate with each key is 
        the timestamp of the tweet 

        :param list_of_timestamps_and_tweets: A list of tuples consisting 
        of a timestamp and a tweet.
        """
        for timestamp, tweet in list_of_timestamps_and_tweets:
            tweet = tweet.lower()
            # check for repeated tweets
            if tweet in self.tweeted_times:
                # save the new tweet if it is more recent
                if self.tweeted_times[tweet] < timestamp:
                    self.tweeted_times[tweet] = timestamp
            else:
                # save the new tweet, if never seen before
                self.tweeted_times[tweet] = timestamp
                self.__process_tweets_helper(tweet)

    def __is_valid_query(self, query):
        """
        If query is Valid, return True if logical operator exist, False otherwise.
        If query is not Valid, raise Exception. 

        :param query: the given query string
        """
        # if logical operators does not exist
        if not re.search(r'[\&\|\!]', query): return False
        # if logical operator exists, query must have the format A Operator B
        if re.search(r'[\&\|]', query) and \
        not re.search(r"(\!\w+|\w+) ([\|\&]) (\!\w+|\w+)", query):
            errors(query)
        # no: word! or word ! or ! word
        if re.search(r'\w+\!|\w+ !|! \w+', query): 
            errors(query)
        # yes: ( ) must exists if both AND and OR operators are found
        if re.search(r'\&', query) and re.search(r'\|', query) \
        and not re.search(r'[\(\)]', query):
            errors(query)
        # no: multiple query words before logical operator, e.i, a b & c d
        if re.search(r"\w+ (\!\w+|\w+) ([\|\&])", query) \
        or re.search(r"([\|\&]) (\!\w+|\w+) (\!\w+|\w+)", query):
            errors(query)
        # check if the parenthesis system was input correctly
        bracket_str = re.sub(r'[\!\&\|\w\d\s]', "", query)
        if not valid_bracket_struct(bracket_str):
            errors(query)
        return True

    def process_queries(self, query):
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
        :return: a dictionary-based set of operations dissected
        from the query
        """
        # delete uneccessary white spaces
        query = re.sub(r'\s\s+', ' ', query)
        logical_exists = self.__is_valid_query(query)

        # query with no logical operator
        instr = None
        if not logical_exists:
            return {'op0': ['&'] + query.split(" ")}

        operations = {}
        op_num = 0
        while logical_exists:
            # process the NOT operator first
            instr = re.search(r'\!\w+', query)
            if instr: 
                operations["op" + str(op_num)] = ['!', instr[0][1:]]
            # process the query in parenthese as soon as possible
            elif re.search(r"[\(\)]", query):
                instr = re.search(r"(?:\(|\(\s)(\w+) ([\|\&]) (\w+)(?:\)|\s\))", query)
                operations["op" + str(op_num)] = [instr[2], instr[1], instr[3]]
            else: # when all parenthese are gone, process left to right
                instr = re.search(r"(\w+) ([\|\&]) (\w+)", query)
                if not instr: break
                operations["op" + str(op_num)] = [instr[2], instr[1], instr[3]]
            # update query
            query = query.replace(instr[0], "op" + str(op_num))
            op_num += 1
        return operations

    def __set_operation(self, operator, set1, set2):
        """
        Perform set operation between two sets with given operator
        :param operator: set operator
        :param set1, set2: two sets to use for the operation
        :return: a set resulted from the operation on set1 using set2
        """
        if operator == "!":
            return set1 - set2
        elif operator == "&":
            return set1 & set2
        return set1 | set2

    def __process_query_word(self, query, instructions):
        """
        Return the sets of tweets associated with the given queries

        :param query: a list represented a dissected section of 
        the original query, 
        represented as [logical operator, word1, word2]
        :param instructions: the set of all instruction dissected
        from the original query
        :return: a list of sets of tweets that satisfied each query, 
        represented as [logical operator, set1, set2]
        """
        for i in range(1, len(query)):
            # check if query is key word used to identify instruction
            if not re.match(r'(op\d+)', query[i]):
                # if not, check if the word was ever tweeted
                try: self.tweeted_words[query[i]]
                # if never tweeted, return an empty set
                except: query[i] = set()
                else: query[i] = self.tweeted_words[query[i]]
            # if yes, return the instruction associated with the query
            else: query[i] = instructions[query[i]]
        return query

    def __search_helper(self, instructions):
        """
        Return all the tweets that satisfied the conditions in the 
        instructions.

        :param instructions: a dictionary all queries
        :return: a set of tweeted words that satisfied the 
        the requirement of the last instructions
        If no such tweet exists, return empty list
        """
        if not instructions: return []
        all_tweets = set(self.tweeted_times.keys())
        results = set()
        # for each instruction
        for stage in instructions:
            log_op = instructions[stage][0]
            # find the sets of tweets or instruction associated with
            # the current instruction
            working_sets = self.__process_query_word(instructions[stage], instructions)
            # execute the instruction
            if len(working_sets) <= 2:
                instructions[stage] = self.__set_operation(log_op, all_tweets, working_sets[1])
            else:
                final_set = working_sets[1]
                for next_set in working_sets[2:]:
                    final_set = self.__set_operation(log_op, final_set, next_set)
                instructions[stage] = final_set
        return instructions['op' + str(len(instructions) - 1)]

    def search(self, query):
        """
        Given a query, for each word in the query, find five 
        different tweets with the highest timestamps.

        :param query: the given query string
        :return: a list of ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        recent_five = []
        instructions = self.process_queries(query.lower())
        found_tweets = list(self.__search_helper(instructions))
        found_tweets.sort(key = lambda x: self.tweeted_times[x], reverse=True)
        # print(found_tweets[:5])
        return found_tweets[:5]
        # for tweet in found_tweets:
        #     if len(recent_five) < 6:
        #         recent_five.append(tweet)
        #     else:
        #         recent_five.append(tweet)
        #         recent_five.sort(key = lambda x: self.tweeted_times[x], reverse=True)
        #         recent_five = recent_five[:-1]
        # return recent_five    

if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/tweets.csv"
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
    ti.search("Neeva & (people | stuffs)")
    ti.search("Neeva people")
    ti.search('hello world')
    ti.search('Neeva & search & ((works | stuff) | !(not & world))')
    ti.search('Neeva & stuffs')
    ti.search('Neeva & !(not | world)')
    # ti.search('Neeva | mine !Google | his Yahoo')
    # ti.search('')