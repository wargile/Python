# happiest_state.py

# Geodata:
# http://www.census.gov/geo/maps-data/index.html

# Google Geocoding:
# https://developers.google.com/maps/documentation/geocoding/
# https://developers.google.com/maps/documentation/geocoding/#ReverseGeocoding
# Google GeoCode API URL:
# https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=API_KEY

# Python pip install:
# http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows?rq=1

import sys
import json
import pprint
import re # for regex
import operator # for sorting tuples in list/dict
# import pygeocoder # https://pypi.python.org/pypi/pygeocoder | pip install pygeocoder

def parsesentiments(fp):
    global scores

    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited.
        scores[term] = int(score)  # Convert the score to an integer.

def displaystates(fp):
    global scores

    stateinfo = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        #'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    #states = {} # Initialize an empty dictionary
    coordinates = {} # Initialize an empty dictionary
    found_states = {} # Initialize an empty dictionary
    tweets = {} # Initialize an empty dictionary
    found_sentiments = {} # Initialize an empty dictionary
    found_states_score = {} # Initialize an empty dictionary
    sentiment_score = 0
    counter = 1
    coord_counter = 1
    pp = pprint.PrettyPrinter(indent = 4)

    for line in fp:
        try:
            # https://docs.python.org/2/library/json.html
            temp = json.loads(line)
            state_found = False
            sentiment_score = 0

            # Get just English language tweets
            if 'lang' in temp and temp['lang'] == 'en':
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
                                    #print sentiment_score
                    except:
                        pass

                if 'place' in temp.keys():
                    try:
                        state = temp['place']['full_name']
                        
                        if state != '':
                            #states[str(counter)] = state
                            #counter = counter + 1

                            for s in stateinfo.keys():
                                wordlist = re.compile("([\w][\w]*'?\w?)").findall(state)
                                for word in wordlist:
                                    if word.upper().find(stateinfo[s].upper()) >= 0 and (len(word) == len(stateinfo[s])):
                                        found_states[stateinfo[s].upper()] = state
                                        # Add the sentiment score to the state
                                        # print "Place: ", stateinfo[s].upper()
                                        if stateinfo[s].upper() in found_states_score.keys():
                                            found_states_score[stateinfo[s].upper()] += sentiment_score
                                        else:
                                            found_states_score[stateinfo[s].upper()] = sentiment_score
                                        state_found = True
                                        break
                    except:
                        pass

                # Just get the lines that have the 'location' key in them:
                if not state_found:
                    if 'user' in temp.keys():
                        try:
                            state = temp['user']['location']

                            if state != '':
                                #states[str(counter)] = state
                                #counter = counter + 1

                                for s in stateinfo.keys():
                                    wordlist = re.compile("([\w][\w]*'?\w?)").findall(state)
                                    for word in wordlist:
                                        if word.upper().find(stateinfo[s].upper()) >= 0 and (len(word) == len(stateinfo[s])):
                                            found_states[stateinfo[s].upper()] = state
                                            # Add the sentiment score to the state
                                            # print "Location: ", stateinfo[s].upper()
                                            if stateinfo[s].upper() in found_states_score.keys():
                                                found_states_score[stateinfo[s].upper()] += sentiment_score
                                            else:
                                                found_states_score[stateinfo[s].upper()] = sentiment_score
                                            state_found = True
                                            break
                        except:
                            pass

                if 'coordinates' in temp.keys(): # TODO: Use as last resort if state still not found above?
                    try:
                        coord = temp['coordinates']
                        if coord != None:
                            coordinates[str(coord_counter)] = temp['coordinates']
                            coord_counter = coord_counter + 1
                    except:
                        pass
        except:
            pass

    # print '--------------------------------------------------------------------\nCoordinates found:\n'
    # pp.pprint(coordinates.items()[1:10])
    # print '--------------------------------------------------------------------\nStates found:\n'
    # pp.pprint(found_states.items())
    # print '--------------------------------------------------------------------\nSorted state scores found:\n'
    
    sorted_scores = sorted(found_states_score.iteritems(), key=operator.itemgetter(1), reverse=True)
    # pp.pprint(sorted_scores)

    state_key, state_value = sorted_scores[0]
 
    for key, value in stateinfo.items():
        # NOTE: Below is the value to print out for assignment!
        if value.upper().find(state_key) == 0:
            print key

# Split a string into separate words (cleaning up), and then merge the array into a string again
def stringsplit(text):
    a = re.compile("([\w][\w]*'?\w?)").findall(text)
    return ' '.join(a)

def main():
    global scores
    scores = {}

    with open(sys.argv[1], 'r') as sentiment_file:
        parsesentiments(sentiment_file)

    with open(sys.argv[2], 'r') as tweet_file:
        displaystates(tweet_file)

if __name__ == '__main__':
    main()
