# Create a Term document Matrix
# -----------------------------
# TODO: Remove all terms that are numeric only?
# TODO: Cosine Similarity (with SVD Single Value Decomposition?) beetween documents
# TODO: Python library nltk has stopwords list etc.

# http://www.slideshare.net/shakthydoss/plagiarism-24203110
# http://en.wikipedia.org/wiki/Tf%E2%80%93idf
# http://en.wikipedia.org/wiki/Stopwords
# http://www.ranks.nl/stopwords
# http://en.wikipedia.org/wiki/Stemming
# http://snowball.tartarus.org/wrappers/guide.html (Stemmer API for Python)
# http://www.tfidf.com/
# https://code.google.com/p/tfidf/
# https://code.google.com/p/stop-words/
# https://code.google.com/p/stop-words/source/browse/#svn%2Ftrunk%2Fstop-words

import math
import re
import numpy as np
import pprint as pp
import pandas as pd
from collections import Counter


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# http://glowingpython.blogspot.no/2011/06/svd-decomposition-with-numpy.html
def svd(A):
    U,s,V = np.linalg.svd(A)
    return U,s,V


# http://stackoverflow.com/questions/10508021/matrix-multiplication-in-python
def cosine_similarity(x, y):
    numerator = 0

    for counter in range(0, len(x)-1):
        numerator = numerator + (x[counter] * y[counter])
        denominator1 = 0
        denominator2 = 0
        for counter in range(0, len(x)-1):
            denominator1 = denominator1 + abs(x[counter]**2)
        for counter in range(0, len(y)-1):
            denominator2 = denominator2 + abs(y[counter]**2)
  
    return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))


def remove_stop_words(text):
    stopwords = {}
    final_wordlist = []

    # http://www.ranks.nl/stopwords
    # TODO: Just load the stopwords once!
    for e, line in enumerate(open("c:/coding/python/stopwords.txt", "rb")):
        line = line.strip()
        stopwords[line] = line

    wordlist = re.compile("([\w][\w]*'?\w?)").findall(text)
    for word in wordlist:
        if not word in stopwords:
            final_wordlist.append(word)

    return " ".join(final_wordlist)
    

def create_tdm():
    tdm_terms = {}
    tdm_corpus = {}
    tdm_corpus_hashed = {} # TODO: Create tf-idf hash with word frequencies for each doc in corpus?
    tdm = {}

    # Put these in Corpus (hash)
    # TODO: 1) Remove stop words (is, of, be, to etc.) from the documents
    #       2) Apply Stemmer to each token in the corpus to remove inflections
    tdm_corpus[0] = "I'm finally starting out. It's cool, cool, cool in the morning..."
    tdm_corpus[1] = "This is very cool! And maybe I'm a Londoner? I love London too!"
    tdm_corpus[2] = "This is maybe not so cool, but way cooler than anything else."
    tdm_corpus[3] = "This is the final straw--but still COOL. Love it! But it's a Catch 22 too."
    tdm_corpus[4] = "This is finally the final straw--but still so COOL. Love it too! But it's a Catch 22."

    tdm_corpus[0] = "x1   x2 None   x4 None"
    tdm_corpus[1] = "None   x2 None   x4   x5"
    tdm_corpus[2] = "x1   x2 None   x4   x5"
    tdm_corpus[3] = "None None None None   x5"
    tdm_corpus[4] = "None   x2   x3   x4   x5"
    tdm_corpus[5] = "x1   x2   x3   x4 None"
    tdm_corpus[6] = "x1   x2   x3   x4   x5"

    folder = "c:/coding/Kaggle/OttoGroupProductClassificationChallenge/Data/"
    df = pd.read_csv('{0}corpus.csv'.format(folder), delimiter=',', header=0, quotechar='"')

    print list(df.columns.values)
    # print [column for column in df]
    # print df.head(n=1)

    print "Calculating the scores..."
    #print(df[0,'Corpus'])

    term_counter = 1

    # Find word occurence in corpus:
    tdm_word_occurence_in_corpus = {}

    for doc in df['Corpus']:
    #for doc in tdm_corpus:
        new_doc = True
        #wordlist = re.compile("([\w][\w]*'?\w?)").findall(tdm_corpus[doc])
        wordlist = re.compile("([\w][\w]*'?\w?)").findall(doc)
        words = set()
        for word in wordlist:
            word = word.lower()
            if word not in words: # Ensure only unique words from the doc are added
                words.add(word)
                if not word in tdm_word_occurence_in_corpus:
                    tdm_word_occurence_in_corpus[word] = 1
                else:
                    if new_doc:
                        tdm_word_occurence_in_corpus[word] += 1
        new_doc = False

    print "Word occurence in corpus:"
    #pp.pprint(tdm_word_occurence_in_corpus)
    df1 = pd.DataFrame(list(tdm_word_occurence_in_corpus.iteritems()), columns=['feature','count'])    
    df1.to_csv('{0}pandas_word_occurence_in_corpus.csv'.format(folder))


    # Create tf-idf hash
    for doc in df['Corpus']:
    #for doc in tdm_corpus:
        tdm_corpus_hashed[doc] = {}
        #wordlist = re.compile("([\w][\w]*'?\w?)").findall(tdm_corpus[doc])
        wordlist = re.compile("([\w][\w]*'?\w?)").findall(doc)
        total = float(len(wordlist))
        for word in wordlist:
            freq = Counter(wordlist)[word]
            word = word.lower() # NOTE: Need to set lower here, so Counter can first find all
            tf = (freq / total)
            docs_with_term = tdm_word_occurence_in_corpus[word]
            idf = math.log(len(wordlist) / float(docs_with_term))
            tf_idf = (tf * idf)
            if not word in tdm_corpus_hashed[doc]:
                tdm_corpus_hashed[doc][word] = [1, tf, idf, tf_idf] # [1=freq, 2=tf, 3=idf, 4=tf-idf]
            else:
                tdm_corpus_hashed[doc][word][0] += 1

    print "tf-idf:"
    #print pp.pprint(tdm_corpus_hashed)
    df2 = pd.DataFrame(list(tdm_corpus_hashed.iteritems()), columns=['feature','count'])    
    df2.to_csv('{0}pandas_tdm_corpus_hashed.csv'.format(folder))
            
    for doc in df['Corpus']:
    #for doc in tdm_corpus:
        #wordlist = re.compile("([\w][\w]*'?\w?)").findall(tdm_corpus[doc])
        wordlist = re.compile("([\w][\w]*'?\w?)").findall(doc)
        for word in wordlist:
            word = word.lower()
            if not word in tdm_terms:
                tdm_terms[word] = 1
            else:
                tdm_terms[word] += 1 # TODO: Only +1 for 1st time occurence of word in document?

    print "Term frequency matrix terms:"
    #pp.pprint(tdm_terms)
    df3 = pd.DataFrame(list(tdm_terms.iteritems()), columns=['feature','count'])    
    df3.to_csv('{0}pandas_tdm_terms.csv'.format(folder))

    n = len(tdm_terms)
    rowcounter = 1
    
    for doc in df['Corpus']:
    #for doc in tdm_corpus:
        tdm_row = [0] * n
        counter = 0
        #wordlist = re.compile("([\w][\w]*'?\w?)").findall(tdm_corpus[doc])
        wordlist = re.compile("([\w][\w]*'?\w?)").findall(doc)
        for term in tdm_terms:
            found = 0
            for word in wordlist:
                if word.lower() == term:
                    found = 1
                    break
            tdm_row[counter] = found
            counter += 1
        tdm[rowcounter] = tdm_row
        rowcounter += 1

    print "Term frequency matrix:"
    #for t in tdm:
    #    print tdm[t]

    df4 = pd.DataFrame(list(tdm.iteritems()), columns=['id','tdm'])    
    df4.to_csv('{0}pandas_tdm.csv'.format(folder)) # TODO: Change sep to ";" here?

    print "Cosine similarity:"
    print cosine_similarity(tdm[1], tdm[2])
    print cosine_similarity(tdm[2], tdm[3])
    print cosine_similarity(tdm[3], tdm[4])
    print cosine_similarity([5,5], [15,15]) # Test OK!
    #print "Single Value Decomposition:"
    #print svd([tdm[3], tdm[4]])
    
if __name__ == '__main__':
    create_tdm()
