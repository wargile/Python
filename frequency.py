# frequency.py

# Assignment 1, problem 4
# https://class.coursera.org/datasci-002/assignment/view?assignment_id=3

import sys
import json
import pprint
import re # for regex

def parsetweets(fp):
    pp = pprint.PrettyPrinter(indent = 4)
    terms = {} # Store counters for the found terms in tweets

    for line in fp:
        try:
            # https://docs.python.org/2/library/json.html
            temp = json.loads(line)
            sentiment_score = 0

            # Just get the lines that have the 'text' key (= the tweet text) in them:
            if 'text' in temp.keys():
                wordlist = re.compile("([\w][\w]*'?\w?)").findall(temp['text'])

                try:
                    for w in wordlist:
                        # TIP: Regarding possible UnicodeWarning raised here:
                        # http://stackoverflow.com/questions/18193305/python-unicode-equal-comparison-failed
                        if not w in terms.keys():
                            terms[w] = 1
                        else:
                            terms[w] += 1
                except:
                    pass
        except:
            pass

    length_terms = len(terms)

    for t in terms.keys():
        print ' '.join([t, str(float(terms[t]) / float(length_terms))])

    #print '--------------------------------------------------------------------\n'
    #pp.pprint(terms.items())

def main():
    with open(sys.argv[1], 'r') as tweet_file:
        parsetweets(tweet_file)

if __name__ == '__main__':
    main()
