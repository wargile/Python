# top_ten.py

# Assignment 1, problem 6
# https://class.coursera.org/datasci-002/assignment/view?assignment_id=3

# Hashtags (if exists) are in ['entities']['hashtags']: 
# "entities":
# {
#     "hashtags":[],
#     "urls":[],
#     "user_mentions":[]
# }

import sys
import json
import pprint
import re # for regex
import operator # for sorting tuples in list/dict

def parsetweets(fp):
    tweets = {} # Initialize an empty dictionary
    counter = 1
    pp = pprint.PrettyPrinter(indent = 4)

    for line in fp:
        # https://docs.python.org/2/library/json.html
        # NOTE: This gets all stuff (tweets, deletes, etc.)
        tweets[str(counter)] = json.loads(line)
        
        if counter > 9:
            break
        else:
            counter = counter + 1

    #print tweets.items()
    
    pp.pprint(tweets['1'])

def displayhashtags(fp):
    hashtags = {} # Initialize an empty dictionary
    counter = 1
    pp = pprint.PrettyPrinter(indent = 4)

    for line in fp:
        try:
            # https://docs.python.org/2/library/json.html
            temp = json.loads(line)

            # Just get the lines that have the 'text' key (= the tweet text) in them:
            if 'entities' in temp.keys():
                try:
                    tags = temp['entities']['hashtags']

                    for tag in tags:
                        # print tag['text']

                        if tag['text'] in hashtags.keys(): # Increase count on existing tag
                            hashtags[tag['text']] = hashtags[tag['text']] + 1
                        else: # Add the new tag
                            hashtags[tag['text']] = 1

                        counter = counter + 1
                except:
                    pass
        except:
            pass

    # Sort the scores in the array, and get top 10 lines (sort DESC)
    # https://docs.python.org/2/howto/sorting.html
    sorted_tags = sorted(hashtags.iteritems(), key=operator.itemgetter(1), reverse=True)
    #print '--------------------------------------------------------------------\n'
    #pp.pprint(sorted_tags[0:10])

    for tag in sorted_tags[0:10]:
        print ' '.join([tag[0], str(tag[1]).strip()]).encode('utf-8')

    # print '--------------------------------------------------------------------\n'
    # pp.pprint(hashtags.items())

def bigrams(text):
    input_list = text.split(' ')
    bigram_list = []

    for i in range(len(input_list) - 1):
        bigram_list.append((input_list[i], input_list[i + 1]))

    return bigram_list

# Split the hashtags into separate words (needed?), and then merge the array into a string again
def stringsplit(text):
    a = re.compile("([\w][\w]*'?\w?)").findall(text)
    return ' '.join(a)

def main():
    with open(sys.argv[1], 'r') as tweet_file:
        displayhashtags(tweet_file)

if __name__ == '__main__':
    main()
