# Functions to split data set based on a field index
# --------------------------------------------------

# import math
# import re
# import numpy as np
# import pprint as pp
# import pandas as pd
# from collections import Counter
# from collections import defaultdict

def splitdata(field_index):
    folder = "C:/coding/Kaggle/Avazu_Click-ThroughRatePrediction/Data/"
    train = "train.csv"
    train_out = "train_out_"
    old_field = ""
    field = ""
    outfile = None

    for e, line in enumerate(open(folder + train, "rb")):
        if e == 0:
            header_line = line
        if e > 0:
            old_field = field
            line = line.strip()
            field = line.split(",")[field_index][0:6]
            if field != old_field:
                if outfile != None:
                    outfile.close()
                print "Opening file:", field
                outfile = open(folder + train_out + field + ".csv", "wb")
                outfile.write(header_line)
            outfile.write(line)

    print "All done!\n"
    
if __name__ == '__main__':
    splitdata(2) # Split on timestamp (day)
