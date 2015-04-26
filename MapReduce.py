# Testing some MapReduce and TF-IDF stuff and other stuff too....

# Tips 'n' tools for test mining:
# http://www.nltk.org/
# http://bommaritollc.com/2011/02/pre-processing-text-rtm-vs-pythonnltk/
# http://www.slideshare.net/japerk/nltk-in-20-minutes
# http://text-processing.com/
# http://streamhacker.com/
# http://knime.com/
# https://my.vertica.com/community/?cmp=70150000000fsNFAAY

# Good for text mining:
# http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC

# In IDLE: 1) import os  2) os.chdir(path)  3) import MapReduce  4) MapReduce.main()
# On command line: python MapReduce.py

# Usage: python MapReduce.py testdata/great_expectations.txt
 
import sys
#import json
import pprint
import re # for regex

def map(docid, content):
    words = {}
    wordlist = re.compile(r"([\w][\w]*'?\w?)").findall(content) # NOTE: r"regex" = raw input
    
    for w in wordlist:
        if not is_number(w):
            if w.lower() in words:
                words[w.lower()] += 1
            else:
                words[w.lower()] = 1

    #return(docid, words)

    for w in words:
        yield(docid, words[w], w)

def reduce():
    pass

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def tf_idf(docid, content):
    words = {}
    wordlist = re.compile(r"([\w][\w]*'?\w?)").findall(content) # NOTE: r"regex" = raw input
    
    for w in wordlist:
        if not is_number(w):
            if w.lower() in words:
                words[w.lower()] += 1
            else:
                words[w.lower()] = 1

    # TF-IDF info: http://www.tfidf.com/
    for w in words:
        words[w.lower()] = "{:.3f}".format((words[w.lower()] / float(len(wordlist)))) # Calculate TF
    
    return(docid, words)

def main():
    pp = pprint.PrettyPrinter(indent=1)
    document1 = "Yeah... I'd say this is a small test document, which is just a test. Which *is* plain awesome!"
    document2 = "Oh, even better! Better and better--and better... Yes indeed, isn't it better than anything else?"

    try:
        with open(sys.argv[1], "r") as fp:
            document3 = fp.read()
    except IOError as e:
        print "I/O error ({0}): {1}: {2}".format(e.errno, e.strerror, sys.argv[1])
        return
        
    freq_list = map("Doc1", document1)
    freq_array = sorted(freq_list, reverse=True) # NOTE: The list is transformed into array
    pp.pprint(freq_array[0:20])
    print "-------------------------------------------------------"
    freq_list = map("Doc1", document1) # TODO: Why must we get the data again here for sorted() to work?
    freq_array = sorted(freq_list, reverse=False) # NOTE: The list is transformed into array
    pp.pprint(freq_array[0:20])
    print "-------------------------------------------------------"

    # Get the TF:
    pp.pprint(tf_idf('Doc1', document1))
    print "-------------------------------------------------------"

    freq_list = map("Doc3", document3)
    #freq_list_temp = freq_list.copy()
    freq_array_desc = sorted(freq_list, reverse=True)
    #freq_array_asc = sorted(freq_list, reverse=False)
    pp.pprint(freq_array_desc[0:30])
    #print "-------------------------------------------------------"
    #pp.pprint(freq_array_asc[0:10])

    freq_hash = {}

    for m in freq_array_desc:
        #print m # Or: m[0], m[1], m[2] to get individual elements
        freq_hash[m[2]] = m

    print "-------------------------------------------------------"
    print "Results for {0}:".format(sys.argv[1])
    #print freq_hash

    key = "cathy"
    try:
        print "Found '{0}' in: {1}".format(key, freq_hash[key])
    except:
        print "Did not find '{0}'!".format(key)

    print "-------------------------------------------------------"

if __name__ == '__main__':
    main()
