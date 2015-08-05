
# coding: utf-8

# # Terje testing some Spark!

# In[1]:

# from pyspark import SparkContext, SparkConf # Already included here
import glob
import re
import operator
from operator import add
from ast import literal_eval


# In[38]:

# https://jupyter.org/
# https://blog.jupyter.org/

import matplotlib.pyplot as plt
# import matplotlib.cm as cm

# Count lines in the novel 'Wuthering Heights'
import os.path
import re

baseDir = os.path.join('data')
inputPath = os.path.join('terje', 'wuthering_heights.txt')
fileName = os.path.join(baseDir, inputPath)

rawData = sc.textFile(fileName, 4).filter(lambda a: len(a.strip()) > 0) # NOTE: Parallelize on 4 nodes
print rawData.take(5)
wutheringHeightsCount = rawData.count()

def parse_string(string_to_parse):
    wordlist = re.compile("([\w][\w]*'?\w?)").findall(string_to_parse)
    return [s.lower() for s in wordlist]

wordList = rawData.flatMap(lambda x: parse_string(x)).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
n = 30
print wordList.takeOrdered(n, key = lambda x: -x[1])
the_wordlist = wordList.takeOrdered(n, key = lambda x: -x[1])

print "Wuthering Heights line count (blank lines omitted):", wutheringHeightsCount

#fig = plt.figure(figsize=(8,4.2), facecolor='white', edgecolor='white')
fig, axes = plt.subplots(figsize=(8.5, 2), frameon=False, facecolor='white', edgecolor='white')
plt.axis([0, n, 0, the_wordlist[0][1]])
plt.grid(b=True, which='major', axis='y', color="#888888", linewidth=.8)
plt.xlabel('Words')
plt.ylabel('Frequency')
barlist = plt.bar(range(n), [freq for (word, freq) in the_wordlist[0:n]], alpha = 0.45, color='#00bbaa')
axes.tick_params(labelcolor='#555555', labelsize='8')
axes.set_title("Wuthering Heights, most frequent words")
axes.set_xticklabels([word for (word, freq) in the_wordlist[0:n]], rotation=45, ha='center')
for axis, ticks in [(axes.get_xaxis(), range(0, n)), (axes.get_yaxis(), range(0, the_wordlist[0][1]+1000, 1000))]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#666666')
pass


# In[8]:

inputPath = os.path.join('terje', 'iis3.log')
fileName = os.path.join(baseDir, inputPath)

rawData = sc.textFile(fileName)
print "Lines in file:" + rawData.count() + "\n"
# Count action: Spark reads in data, sums within partitions (1 in this example), and combines result in driver

errors = rawData.filter(lambda line: "139.116.15.40" in line).collect()
print errors[1:3]
errors = rawData.filter(lambda line: line.startswith("139.116.15.37,POSTEN")).collect()
print len(errors)
# rawData.filter(lambda x: x.contains("LMKBRUKER")).count()


# In[7]:

# More 'Wuthering Heights' manipulation - counting and sorting word requency
inputPath = os.path.join('terje', 'wuthering_heights.txt')
outputPath = os.path.join('terje', 'wuthering_heights_out1')

fileName = os.path.join(baseDir, inputPath)
fileNameOut = os.path.join(baseDir, outputPath)

rawData = sc.textFile(fileName) # NOTE: No parallelization, 1 results file created
# wc = rawData.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
# wc = rawData.flatMap(lambda x: re.compile("([\w][\w]*'?\w?)").findall(x)).map(lambda x: (x, 1)).reduceByKey(add)
wc = rawData.flatMap(lambda x: [x.lower() for x in re.compile("([\w][\w]*'?\w?)").findall(x)]).map(lambda x: (x, 1)).reduceByKey(add)
# re.compile("([\w][\w]*'?\w?)").findall("This is so cool!")

wc.saveAsTextFile(fileNameOut)
print "Textfile saved!"


# In[135]:

n = 30
fig, axes = plt.subplots(figsize=(8.5, 2), frameon=False, facecolor='white', edgecolor='white')
fig.set_frameon(False) # ??
axes.tick_params(labelcolor='#555555', labelsize='8')
plt.bar(range(n), [freq for (word, freq) in words_sorted[0:n]], alpha = 0.5)
#plt.grid(color="#bbbbbb", linewidth=.8, linestyle='-')
max_y = words_sorted[0][1]
for axis, ticks in [(axes.get_xaxis(), range(0, n)), (axes.get_yaxis(), range(0, max_y, 1000))]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#666666')
axes.set_title("Wuthering Heights, most frequent words")
axes.set_xticklabels([word for (word, freq) in words_sorted[0:n]], rotation=45, ha='center')
plt.show()


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


# ### Week 2 lectures
# ### -----------------------

# In[12]:

rdd = sc.parallelize(range(1, 26, 1))
# No computation happens, lazy evaluation. Spark saves the "recipe" for creating the result here
result = rdd.map(lambda x: x * 2).collect() # lambdas are closures/actions passed to workers
print result


# In[14]:

result = rdd.filter(lambda x: x % 3 == 0).collect()
print result


# In[21]:

mydata = range(1, 13, 1) + range(1, 16, 1)
print mydata
rdd2 = sc.parallelize(mydata)
print rdd2.distinct().collect()


# In[25]:

print rdd2.map(lambda x: [x, x + 5]).collect()
print rdd2.flatMap(lambda x: [x, x + 5]).distinct().collect()


# In[4]:

rdd3 = sc.parallelize([1,2,3,4,5,6,7,8])
result = rdd3.reduce(lambda a, b: a * b)
print(1*2*3*4*5*6*7*8)
print result


# In[9]:

rdd4 = sc.parallelize([5,8,1,2,10,17])
rdd4.takeOrdered(3, lambda s: -1 * s) # Take 3 elements, DESC sorting


# In[3]:

rdd5 = sc.parallelize([(1,'a'), (2,'b'), (3,'c'),(2,'d'),(2,'e')]) # Key-Value pairs, a Pairs RDD, each element is a pair tuple
print rdd5.sortByKey().collect()


# In[6]:

rdd6 = sc.parallelize([(1,1), (2,2), (3,3), (2,2), (2,2)]) # Key-Value pairs, a Pairs RDD, each element is a pair tuple
print rdd6.reduceByKey(lambda a, b: a * b).collect()


# In[22]:

rdd7 = sc.parallelize([(1,'a'), (2,'b'), (3,'c'),(2,'d'),(2,'e')]) # Key-Value pairs, a Pairs RDD, each element is a pair tuple
result = rdd7.groupByKey().partitionBy(1).map(lambda x: sorted(x[1].data)).collect()
# Be careful, as groupByKey can cause a lot of data movement on huge arrays
#result
for x in result:
    print x


# ## pySpark shared variables
# ### Broadcast variables
# Efficiently send large, read-only variable to workers
# Saved at workers to use in one or more Spark operations
# It's like sending a large, read-only lookup table to all workers
# ### Accumulators
# Aggregate values from workers back to driver
# Only driver can access value from accumulator
# For tasks, accumulators are write-only
# Use to count errors seen in RDD across all workers
# 
# In iterative or repeated computations, broadcast variables avoid the problem of SENDING the SAME data to workers.
# Accumulators can NOT be used by Spark workers to efficiently READ values during distributed computations.

# In[87]:

my_huge_dict = {'a': 20, 'b': 30, 'd': 50}
broadcastVar = sc.broadcast(my_huge_dict) # Read-only, sent to all workers in a closure
broadcastVar.value
my_letters = sc.parallelize(['a','b','c','d','e'])

def my_lookup_function(letter):
    a = 0
    if letter in broadcastVar.value:
        a = broadcastVar.value[letter]
    return a

letter_count = my_letters.map(my_lookup_function).collect()
print letter_count


# In[65]:

# Using accumulators
inputPath = os.path.join('terje', 'wuthering_heights.txt')
fileName = os.path.join(baseDir, inputPath)

rawData = sc.textFile(fileName) # NOTE: No parallelization, 1 results file created
# print rawData
blankLines = sc.accumulator(0) # Init

def countBlankLines(line):
    global blankLines # Important!
    if len(line.strip()) == 0:
        blankLines += 1

blankLinesCount = rawData.foreach(countBlankLines)
print "Number of blank lines in 'Wuthering Heights' is %d" % blankLines.value


# In[59]:

blankLines = sc.accumulator(0) # Init
rawData = sc.parallelize(["A line", "", "another line", "yes", "", "", "Last one!"])
def f(line):
    global blankLines
    if len(line.strip()) == 0:
        blankLines += 1 # Seen at worker as a write-only variable, can NOT see the value!
    
rawData.foreach(f)
print "Number of blank lines is %d" % blankLines.value


# In[75]:

accum = sc.accumulator(0)
sc.parallelize(range(1, 10, 1)).foreach(lambda x: accum.add(x))
print accum.value


# In[7]:

import string
#string.split("This    is a string... yes")
print len("This    is a string... yes".split())


# In[26]:

# TIP: Use https://regex101.com/ to test your regex!
import re
pattern = '^(\S+) "(\S*)(\s?)"'
match = re.search(pattern, 'Balle "Klorin "')
#match = re.search(pattern, 'Balle "Klorin"')
print match.group(1) + "#" + match.group(2)


# In[2]:

my_list = []
my_tuple = ('Testing tuple', 22)
my_list.append(my_tuple)
print my_list


# In[3]:

my_tuples = [('One', 1), ('Two', 2), ('Three', 3)]
print dict(my_tuples)


# In[ ]:



