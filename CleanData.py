# Functions to clean data set for Kaggle Timeshift Text Classification competition
# --------------------------------------------------------------------------------

# import math
# import re
# import numpy as np
# import pprint as pp
# import pandas as pd
# from collections import Counter
from collections import defaultdict

folder = "C:/coding/Kaggle/TradeshiftTextClassification/Data/"
train = "train.csv"
train_out = "train_out.csv"
test = "test.csv"
test_out = "test_out.csv"

n = 1000000 # Breakout counter
n = 1000 # Breakout counter

doc_elements = defaultdict(float) # For counting identical base64 hashes
hashes = defaultdict()

def cleandata(location, dataset, dataset_out):
    hash_no = 0

    for e, line in enumerate(open(location + dataset, "rb")):
        if e > 0: # Skip header line
            row = line.strip().split(",")
            for field in row[1:]: # Skip id field
                if "=" in field:
                    doc_elements[field] += 1
                    if not hash(field) in hashes:
                        hashes[hash_no] = hash(field)
                        hash_no += 1
        if e % 10000 == 0:
            print "%d rows done..." % e 
        if e >= n:
            break

    #print hashes # Too many....

    with open(location + dataset_out, "wb") as outfile:
        for e, line in enumerate(open(location + dataset, "rb")):
            fields_out = []
            row = line.strip().split(",")
            if e == 0:
                outfile.write(",".join(row[1:]))
            else:
                for field in row[1:]: # NOTE: Skipping id field
                    if "=" in field:
                        if field in doc_elements:
                            fields_out.append(doc_elements[field])
                        else:
                            fields_out.append(0.0)
                    elif field == "YES":
                        fields_out.append(1.0)
                    elif field == "NO":
                        fields_out.append(0.0)
                    elif field == "":
                        fields_out.append(-1.0) # Or -999 or something else?
                    else:
                        fields_out.append(float(field))
                        
            outfile.write("%s\n" % ",".join([str(f) for f in fields_out]))
            
            if e % 10000 == 0:
                print "%d rows done..." % e 
            if e >= n:
                break

    print "All done!\n"
    
if __name__ == '__main__':
    #cleandata(folder, train, train_out)
    cleandata(folder, test, test_out)
