
# coding: utf-8

# # Terje testing some Spark!

# In[10]:

# from pyspark import SparkContext, SparkConf # Already included here
import glob
import re
import operator
from operator import add
from ast import literal_eval


# In[2]:

# https://jupyter.org/
# https://blog.jupyter.org/

# Count words in the novel 'Wuthering Heights'
import os.path
baseDir = os.path.join('data')
inputPath = os.path.join('terje', 'wuthering_heights.txt')
fileName = os.path.join(baseDir, inputPath)

rawData = sc.textFile(fileName)
wutheringHeightsCount = rawData.count()

print "Wuthering Heights words:", wutheringHeightsCount


# In[8]:

inputPath = os.path.join('terje', 'iis3.log')
fileName = os.path.join(baseDir, inputPath)

rawData = sc.textFile(fileName)

errors = rawData.filter(lambda line: "139.116.15.40" in line).collect()
print errors[1:3]
errors = rawData.filter(lambda line: line.startswith("139.116.15.37,POSTEN")).collect()
print len(errors)
# rawData.filter(lambda x: x.contains("LMKBRUKER")).count()


# In[46]:

# More 'Wuthering Heights' manipulation - counting and sorting word requency
inputPath = os.path.join('terje', 'wuthering_heights.txt')
outputPath = os.path.join('terje', 'wuthering_heights_out1')

fileName = os.path.join(baseDir, inputPath)
fileNameOut = os.path.join(baseDir, outputPath)

rawData = sc.textFile(fileName)
# wc = rawData.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
# wc = rawData.flatMap(lambda x: re.compile("([\w][\w]*'?\w?)").findall(x)).map(lambda x: (x, 1)).reduceByKey(add)
wc = rawData.flatMap(lambda x: [x.lower() for x in re.compile("([\w][\w]*'?\w?)").findall(x)]).map(lambda x: (x, 1)).reduceByKey(add)
# re.compile("([\w][\w]*'?\w?)").findall("This is so cool!")

wc.saveAsTextFile(fileNameOut)


# In[66]:

outputPathSorted = os.path.join('terje', 'wuthering_heights_sorted.txt')
fileNameOutSorted = os.path.join(baseDir, outputPathSorted)

files = glob.glob(fileNameOut + "/part-*")
words = []
for f in files:
    for e, line in enumerate(open(f, "rb")):
        words.append(tuple(literal_eval(line.strip())))

# words_sorted = sorted(words, key=operator.itemgetter(1, 0), reverse=True) # Sort on 1) frequency 2) word
words_sorted = sorted(words, key = lambda x: (-x[1], x[0]))
print words_sorted[0:20] # Print some of the highest frequencies

f = open(fileNameOutSorted, "wb")
for w, freq in words_sorted:
    f.write(w + ";" + str(freq) + "\n")
    
f.close()


# In[103]:

import matplotlib.pyplot as plt
import matplotlib.cm as cm

n = 30
fig, axes = plt.subplots(figsize=(8.5, 2), facecolor='white', edgecolor='white')
axes.tick_params(labelcolor='#555555', labelsize='8')
plt.bar(range(n), [freq for (word, freq) in words_sorted[0:n]], alpha = 0.5)
plt.title = "Wuthering Heights, most frequent words"
plt.grid(color="#bbbbbb", linewidth=.8, linestyle='-')
for axis, ticks in [(axes.get_xaxis(), range(0, n)), (axes.get_yaxis(), range(0, 5000, 1000))]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#666666')
axes.set_xticklabels([word for (word, freq) in words_sorted[0:n]], rotation=90, ha='center')
plt.show()


# In[ ]:



