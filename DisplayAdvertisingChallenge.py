# DisplayAdvertisingChallenge.py
# C:/coding/Kaggle/DisplayAdvertisingChallenge/code/DisplayAdvertisingChallenge.py

# TIPS:
# CTR:
# It depends how the CTR is calculated (averaging size).
# My approach was moving average like this:
# double CTR = 0.0, decay = 0.9999;
# for (uint i=0; i < rowCnt; i++)
#   CTR = decay*CTR + (1.0-decay)*targets[i];
  
# CTR = click-through-rate: http://en.wikipedia.org/wiki/Click-through_rate
# http://blog.yhathq.com/posts/logistic-regression-and-python.html
# http://www.kaggle.com/c/criteo-display-ad-challenge/forums/t/9561/how-to-apply-python-linear-model-sgdregressor-to-do-logistic-regression/51205#post51205
# http://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
# R glmnet: http://blog.revolutionanalytics.com/2013/05/hastie-glmnet.html

#import os
#import pprint
#import operator
#import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import random

maxrows = 0
rows = []
randomrows_hash = {} # Much faster lookup than with list
rownum = 0
subset = 1500000
infile = 'C:/coding/Kaggle/DisplayAdvertisingChallenge/data/train.csv'
outfile = 'C:/coding/Kaggle/DisplayAdvertisingChallenge/data/train_out.csv'

print "Starting..."

with open(infile, 'rb') as f_in:
    header = f_in.readline()
    while f_in.readline():
        maxrows += 1
        if not (maxrows % 1000000):
            print "Read {0} rows...".format(maxrows)

print "Input file read. Lines: {0}".format(maxrows)

randomrows = [random.randint(2, maxrows) for _ in xrange(subset)]
print 'Len: ', len(randomrows)

# Add rows to hash for faster lookup
for row in randomrows:
    randomrows_hash[str(row)] = row

rownum = 0

with open(outfile, 'wb') as f_out:
    with open(infile, 'rb') as f_in:
        f_out.write(header.encode('UTF-8'))
        while True:
            row = f_in.readline()
            if not row:
                break
            rownum += 1
            if str(rownum) in randomrows_hash:
                f_out.write(row.encode('UTF-8'))
                if not (rownum % 10000):
                    print "Found row {0}...".format(rownum)

df = pd.read_csv(outfile, sep=',', header=1)

print "-----------\n", df.head(n=1)
# df.columns = ["col1", "col2", "col3"]
# print df.describe()
