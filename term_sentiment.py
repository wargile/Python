# term_sentiment.py

# Assignment 1, problem 3
# https://class.coursera.org/datasci-002/assignment/view?assignment_id=3

# TIPS:
# https://class.coursera.org/datasci-002/forum/thread?thread_id=289
# https://class.coursera.org/datasci-002/forum/thread?thread_id=493
# http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
# http://www.umiacs.umd.edu/~saif/WebPages/Abstracts/NRC-SentimentAnalysis.htm
# https://github.com/tlfvincent/StatOfMind/blob/master/Sentiment_Analysis_of_TV_shows/get_epsiode_transcripts.py

import sys
import json
import pprint
import re # for regex

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
    found_non_sentiments = {} # Store counters for the found non-sentiments in tweets
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

                    # Store the tweet's sentiment score and word count for each of the non-sentiment words found 
                    for w in wordlist:
                        if not w in scores.keys():
                            if not w in found_non_sentiments.keys():
                                found_non_sentiment = {'count':1, 'score':sentiment_score, 'final_score':float(0.0)}
                                found_non_sentiments[w] = found_non_sentiment
                            else:
                                found_non_sentiments[w]['found_non_sentiment']['count'] += 1
                            
                    #print sentiment_score
                except:
                    pass
        except:
            pass

    # Compute final score
    for f in found_non_sentiments:
        found_non_sentiments[f]['final_score'] = \
        found_non_sentiments[f]['score'] / \
        float(found_non_sentiments[f]['count'])

    #print '--------------------------------------------------------------------\n'
    #pp.pprint(tweets.items())
    #pp.pprint(scores.keys())
    #pp.pprint(found_non_sentiments)

    for f in found_non_sentiments: # Note: This gives keys() by default
        print ' '.join([f, str(found_non_sentiments[f]['final_score'])]).encode('utf-8')
        # TIP: print "%s %.4f" % (word, freq)

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
    global scores # Initialize an empty dictionary for the sentiment scores
    scores = {}

    with open(sys.argv[1], 'r') as sent_file:
        parsesentiments(sent_file)

    with open(sys.argv[2], 'r') as tweet_file:
        parsetweets(tweet_file)

if __name__ == '__main__':
    main()
