
# coding: utf-8

# In[1]:

import os
#import sys
import glob
import re
import math
import matplotlib.pyplot as plt
#import operator
from operator import add
from pyspark import SparkContext, SparkConf
#from ast import literal_eval

# Line below is not necessary, as Spark shell pre-loads the SparkContext sc object
# sc = SparkContext( 'local', 'pyspark')

get_ipython().magic(u'matplotlib inline')

spark_home = os.environ.get('SPARK_HOME', None)
print('The SPARK home directory is: ' + spark_home)


# In[34]:

# Use README.md from Spark home dir
# text_file = sc.textFile(spark_home + '\\README.md')
# Use Shakespeare.txt from c:/coding/hadoop/pig/MapReduceInputData
text_file = sc.textFile('C:\coding\Hadoop\pig\MapReduceInputData\CompleteShakespeare.txt')


# In[44]:

# Get separate words by regex, lowercase 'em, count 'em and sort 'em DESC
word_counts = text_file     .flatMap(lambda line: [w.lower() for w in re.compile("([\w][\w]*'?\w?)").findall(line)])     .map(lambda word: (word, 1))     .reduceByKey(lambda a, b: a + b).map(lambda (a, b): (b, a)).sortByKey(False, 1).map(lambda (a, b): (b, a))

n = 35
print word_counts.collect()[0:n]
highfreq_words = word_counts.collect()[0:n]
words = [w for (w, f) in highfreq_words]
frequency = [f for (w, f) in highfreq_words]


# In[45]:

# Plot a figure of highest freq. words
fig, axes = plt.subplots(figsize=(15, 4), frameon=False, facecolor='white', edgecolor='white')
plt.axis([0, len(words), 0, max(frequency)])
plt.grid(b=True, which='major', axis='y')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.bar(range(0, len(frequency)), frequency, alpha=0.75, color='#00bbaa')

y_axis_interval = int(math.floor(max(frequency) / 5))
for axis, ticks in [(axes.get_xaxis(), range(0, len(words))), (axes.get_yaxis(), range(0, max(frequency), y_axis_interval))]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#666666')

axes.set_title("Readme.md, most frequent words")
axes.set_xticklabels(words, rotation=35, ha='right')

plt.show()


# In[ ]:



