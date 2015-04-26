# tweet_sentiment.py

# Assignment 1, problem 2
# https://class.coursera.org/datasci-002/assignment/view?assignment_id=3

# TIPS: https://class.coursera.org/datasci-002/forum/thread?thread_id=407

import sys
import json
import pprint
import re # for regex

def lines(fp):
    print str(len(fp.readlines()))

def parsesentiments(fp):
    global scores

    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited.
        scores[term] = int(score)  # Convert the score to an integer.

def parsetweets(fp):
    global scores

    pp = pprint.PrettyPrinter(indent = 4)
    tweets = {} # Initialize an empty dictionary
    found_sentiments = {} # Store counters for the found sentiments in tweets
    counter = 1

    for line in fp:
        try:
            # https://docs.python.org/2/library/json.html
            temp = json.loads(line)
            sentiment_score = 0

            # Just get the lines that have the 'text' key (= the tweet text) in them:
            if 'text' in temp.keys():
                tweets[str(counter)] = temp['text'] #.encode('utf-8')
                wordlist = re.compile("([\w][\w]*'?\w?)").findall(temp['text'])
                counter = counter + 1

                try:
                    for w in wordlist:
                        # TIP: Regarding UnicodeWarning raised here:
                        # http://stackoverflow.com/questions/18193305/python-unicode-equal-comparison-failed
                        if w in scores.keys():
                            if not w in found_sentiments.keys():
                                found_sentiments[w] = scores[w]
                                sentiment_score = scores[w]
                            else:
                                found_sentiments[w] += scores[w]
                                sentiment_score += scores[w]
                                
                    print sentiment_score
                except:
                    pass
        except:
            pass

    #print '--------------------------------------------------------------------\n'
    #pp.pprint(tweets.items())
    #pp.pprint(scores.keys())
    #pp.pprint(found_sentiments)

def bigrams(text):
    input_list = text.split(' ')
    bigram_list = []

    for i in range(len(input_list) - 1):
        bigram_list.append((input_list[i], input_list[i + 1]))

    return bigram_list

# Split the tweet into separate words (cleaned up), and then merge the array into a string again
def stringsplit(text):
    a = re.compile("([\w][\w]*'?\w?)").findall(text)
    return ' '.join(a)

def main():
    # sent_file = open(sys.argv[1])
    # tweet_file = open(sys.argv[2])

    global scores # Initialize an empty dictionary for the sentiment scores
    scores = {}

    # Other way, ensures file closes at end, even if error occurs:
    # with open(sys.argv[1], 'r') as sent_file:
    #    lines(sent_file)

    # with open(sys.argv[2], 'r') as tweet_file:
    #    lines(tweet_file)

    with open(sys.argv[1], 'r') as sent_file:
        parsesentiments(sent_file)

    with open(sys.argv[2], 'r') as tweet_file:
        parsetweets(tweet_file)

    # Create the 20-line submission file (NOTE: Remove this block for final submission)
    """
    with open(sys.argv[2], 'r') as tweet_file:
        out_file = open('problem_1_submission.txt', 'w')
        counter = 0

        for line in tweet_file:
            if counter == 20:
                break
            else:
                out_file.write(line.encode('utf-8'))

            counter = counter + 1

        out_file.close()
    """

if __name__ == '__main__':
    main()
