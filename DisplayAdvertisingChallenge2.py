# DisplayAdvertisingChallenge2.py
# C:/coding/Kaggle/DisplayAdvertisingChallenge/code/DisplayAdvertisingChallenge2.py
# Deadline 23.08.2014

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

limitrows = True
readrows = 1500000
interval = 10000
maxrows = 0
imputeval = '0'

infile = 'C:/coding/Kaggle/DisplayAdvertisingChallenge/data/train_out.csv'
outfile = 'C:/coding/Kaggle/DisplayAdvertisingChallenge/data/train_fixed.csv'
startcol = 2 # 2 for train, 1 for test
#infile = 'C:/coding/Kaggle/DisplayAdvertisingChallenge/data/test.csv'
#outfile = 'C:/coding/Kaggle/DisplayAdvertisingChallenge/data/test_fixed.csv'
#startcol = 1 # 2 for train, 1 for test

def normalize(minval, maxval, minnorm, maxnorm, curval):
    # Find the normalized (0-1 range) value of curval
    normalized = (curval - minval) / (maxval - minval)
    # print normalized
    # Now let's get the new normalized value adjusted for our minnorm and maxnorm params
    normval = minnorm + ((maxnorm - minnorm) * normalized)
    return (normval)

print "Starting..."

with open(infile, 'rb') as f_in:
    with open(outfile, 'wb') as f_out:
        header = f_in.readline().rstrip() # NOTE: To avoid ^M char
        colnames = header.split(',')
        print colnames, len(colnames)
        f_out.write('{0}\r\n'.format(header).encode('UTF-8'))
        while True:
            row = f_in.readline()
            if not row:
                break
            maxrows += 1
            fields = row.split(',')
            colcounter = startcol
            newfields = []
            newfield = ''
            for col in colnames[startcol:len(colnames)]:
                if col[0] == 'C':
                    try:
                        newfield = str(long(fields[colcounter].strip(), 16))
                        #print newfield
                        # TODO: Normalize data
                    except:
                        newfield = imputeval
                        #print '---> NA'
                        pass
                else:
                    try:
                        if len(fields[colcounter].strip()) > 0:
                            newfield = fields[colcounter].strip()
                            # TODO: Normalize data
                        else:
                            newfield = imputeval
                            #print '---> NA'
                    except:
                        newfield = imputeval
                        #print '---> NA'
                        pass
                colcounter += 1
                newfields.append(newfield)
            #print len(newfields), "\n"
            if startcol == 2: # train set
                f_out.write('{0},{1},'.format(fields[0], fields[1]).encode('UTF-8'))
            else: # test set
                f_out.write('{0},'.format(fields[0]).encode('UTF-8'))
            for counter in range(0, len(newfields)-1): # Note: Range max is max-1!
                f_out.write('{0},'.format(newfields[counter]).encode('UTF-8'))
            f_out.write('{0}\r\n'.format(newfields[len(newfields)-1]).encode('UTF-8'))
            if maxrows >= readrows and limitrows:
                break
            if not (maxrows % interval):
                print "Read {0} rows...".format(maxrows)

print "Done!"
