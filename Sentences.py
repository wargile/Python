# Functions to clean data set for Kaggle Timeshift Text Classification competition
# --------------------------------------------------------------------------------
# Run from Git Bash:
# Cut id field and sort the file:
# cut -d ' ' -f 2- sentences.txt | sort > sentences.sorted.txt
# Just sort the file:
# sort sentences.txt > sentences.sorted.txt

# http://norvig.com/spell-correct.html

# import math
# import re
# import numpy as np
# import pprint as pp
# import pandas as pd
import difflib
# from collections import Counter
from collections import defaultdict

folder = "C:/coding/R/Coursera/MiningOfMassiveDatasets/Week 3/ProgrammingAssignment/"
filename_in = "sentences.txt"
filename_out = "sentences_cleaned.txt"
filename_sorted_out = "sentences_sorted.txt"
filename_matrix_out = "sentences_matrix.txt"

filename_in = "sentences_test.txt"
filename_out = "sentences_cleaned_test.txt"
filename_sorted_out = "sentences_sorted_test.txt"
filename_matrix_out = "sentences_matrix_test.txt"

n = 10000000 # Breakout counter for test
#n = 100000 # Breakout counter for test
breaks = 100000
unique_sentences = defaultdict()
universal_set = defaultdict()
input_matrix = defaultdict()
signatures = defaultdict()
duplicates = defaultdict()

def intersect(a, b):
    # return [val for val in a if val in b]:
    return list(set(a) & set(b))

def compare_arrays(a, b):
    d = difflib.Differ()
    list(d.compare(a, b))

def hash_it(filename_out):
    pass

def remove_duplicates(location, filename_in, filename_out):
    total_pairs = 0
    
    with open(location + filename_out, "wb") as outfile:
        for e, line in enumerate(open(location + filename_in, "rb")):
            # Get id part
            pos = line.find(" ")
            line_id = line[0:pos]
            line = line[pos + 1: ]
            # Get row after id part

            if not line in unique_sentences:
                unique_sentences[line] = line
                outfile.write("%s %s" % (line_id, line))
            
            if line in duplicates:
                duplicates[line].append(line_id)
            else:
                duplicates[line] = []
                duplicates[line].append(line_id)

            if e % breaks == 0:
                print "%d rows done..." % e 
            if e >= n:
                break

    print "All done!"
    # TODO: Need to find all unique duplicates (keys) to get pairs pr. key:
    for k in duplicates.values():
        if len(k) > 1:
            total_pairs += (len(k) * (len(k) - 1)) / 2
            #print k
    print "Duplicates found:", total_pairs
    
def create_universal_set(location, filename_in):
    counter = 0
    for e, line in enumerate(open(location + filename_in, "rb")):
        row = line.strip().split(" ")
        for word in row[1:]: # Skip id field
            if not word in universal_set:
                counter = counter + 1
                universal_set[word] = counter
        if e % breaks == 0:
            print "%d rows done..." % e 
        if e >= n:
            break

    print "All done!\nTotal number of words:", len(universal_set)

def create_input_matrix(location, filename_in, filename_matrix_out):
    with open(location + filename_matrix_out, "wb") as outfile:
        for e, line in enumerate(open(location + filename_in, "rb")):
            row = line.strip().split(" ")
            id = row[0] # save id field
            matrix_row = []
            for word in row[1:]: # Skip id field
                matrix_row.append(universal_set[word])
            input_matrix[id] = matrix_row
            outfile.write("%s\n" % matrix_row)
            if e % breaks == 0:
                print "%d rows done..." % e 
                if e >= n:
                    break

    print "All done!\n"
    print "Input_matrix row 0     :", input_matrix["0"]
    print "Input_matrix row 1     :", input_matrix["1"]
    print "Input_matrix row 111   :", input_matrix["111"]
    print "Input_matrix row 222   :", input_matrix["222"]

def hash_into_buckets(input_matrix):
    def h(x):
        return x % 5
    def g(x):
        return ((2 * x) + 1) % 5
  
    n = len(input_matrix)
    sig1 = [float("inf"), float("inf")]
    final_sig1 = [float("inf"), float("inf")]
  
    # for counter in range(0, n + 1):
    for counter in range(0, 10):
        column = input_matrix[str(counter)]
        for cell in column: 
            sig1 = [h(cell), g(cell)]
        if sig1[0] < final_sig1[0]:
            final_sig1[0] = sig1[0]
        if sig1[1] < final_sig1[1]:
            final_sig1[1] = sig1[1]
        signatures[counter] = [final_sig1, final_sig2]


if __name__ == '__main__':
    remove_duplicates(folder, filename_in, filename_out)
    create_universal_set(folder, filename_out)
    create_input_matrix(folder, filename_out, filename_matrix_out)
    # hash_into_buckets(input_matrix)
    
    # print signatures[0]
