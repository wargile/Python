# Using pandas for fast CSV read

#import os
#import operator
#import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
import re
import pprint
import csv

sorted_list = []
goodwords = {}
numrows = 0
counter = 0
folder = 'C:/coding/Kaggle/RandomActsOfPizza/data/'

pp = pprint.PrettyPrinter(indent=1)

df = pd.read_csv('{0}Pizza.csv'.format(folder),
                 delimiter='#', header=0, quotechar='"')

# print list(df.columns.values)
# print [column for column in df]
# print df.head(n=1)

print "Calculating the scores..."

for w in df['x']:
    try:
        wordlist = re.compile("([\w][\w]*'?\w?)").findall(w)
        counter += 1
        
        for word in wordlist:
            word = re.sub('[_\']', '', word)
            # re.compile(r'(\w)(\1{2,})').findall(word)
            if (not word.isdigit()) and (len(word) > 0) and (not re.search("\d", word)):
                if word in goodwords:
                    goodwords[word] += 1
                else:
                    goodwords[word] = 1
    except:
        print w
        pass

print "Sorting the scores..."

for word in goodwords:
    (value, key) = goodwords[word], word
    sorted_list.append((value, key))
    
#pp.pprint(sorted(sorted_list, reverse=True))

df_texts = pd.read_csv('{0}PizzaTexts_test.csv'.format(folder),
                 delimiter='#', header=0, quotechar='"')
df_score = pd.read_csv('{0}goodwords_final.txt'.format(folder),
                       delimiter=',', header=0, quotechar='\'')

goodwords = {}

print "Looking up the scores..."

for index, row in df_score.iterrows():
    goodwords[row['Word']] = int(row['Freq'])

# Add a score column to the df_texts dataframe:
df_texts['score'] = 0
# Create index in id (NOTE: Returns the updated dataframe!):
df_texts = df_texts.set_index(df_texts['id'], drop=True)

for index, row in df_texts.iterrows():
    wordlist = re.compile("([\w][\w]*'?\w?)").findall(row['text'])
    scores = {}
    for word in wordlist:
        if word in goodwords:
            if not word in scores:
                scores[word] = int(goodwords[word])
    score_final = 0
    for score in scores:
        score_final += int(scores[score])
    df_texts['score'][row['id']] = score_final

#for index, row in df_texts.iterrows():
#    print row['id'], row['score']

df_texts.to_csv(path='{0}PizzaTexts_out.csv'.format(folder),
                sep=',', header=True, index=True, quoting=csv.QUOTE_NONNUMERIC)

print "All done!"
