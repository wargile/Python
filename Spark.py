'''
Spark GUI for monitoring jobs, etc.: http://localhost:4040

Running applications: ./bin/run-example SparkPi 10
Examples for streaming/MLib (NOTE: These can not run in the shell) must be deployed as a jar (Maven/SBT to build?)

TODO: Steps to install Zulu/Azul Java implementation
-----------------------------------------------------------------
Install SBT:
http://www.scala-sbt.org/download.html

Adjust: sbt/conf/sbtconfig.txt (where is that file now?? C:\Users\tbak\.sbt\0.13 ??):
-Xmx1024M, -XX:MaxPermSize=256m, -XX:ReservedCodeCacheSize=128m
libraryDependencies += "org.apache.spark" % "spark-streaming_2.10" % "1.2.1"
-----------------------------------------------------------------
Getting and building Spark on Windows:
(https://spark.apache.org/downloads.html)
(NOTE: Relies on Azul/Zulu Java implementation being present)
cd c:/
git clone https://github.com/apache/spark
REM or:
git clone git://github.com/apache/spark.git -b branch-1.3
cd spark
sbt/sbt assembly
-----------------------------------------------------------------
# NOTE: Fix for 'winutils not found' error on Spark on Win7:
# http://qnalist.com/questions/4994960/run-spark-unit-test-on-windows-7
# https://social.msdn.microsoft.com/forums/azure/en-US/28a57efb-082b-424b-8d9e-731b1fe135de/please-read-if-experiencing-job-failures?forum=hdinsight
-----------------------------------------------------------------
Spark in Hortonworks Sandbox:
http://hortonworks.com/hadoop-tutorial/using-apache-spark-hdp/
http://clarkupdike.blogspot.no/2014/12/running-spark-on-yarn-from-outside.html
-----------------------------------------------------------------
Run spark/ec2/spark-ec2-script
Run om demand or spot instances on EC2 (spot instances are cheap?) Specify node type, number of nodes
Quick, low cost proof of concept
-----------------------------------------------------------------
Scala mode Emacs:
https://github.com/hvesalai/scala-mode2
-----------------------------------------------------------------
Strata + Hadoop 2015:
https://www.youtube.com/watch?v=1KvTZZAkHy0
-----------------------------------------------------------------
Spark Summit East 2015, slides and PDF's:
http://spark-summit.org/east/2015
https://www.youtube.com/watch?v=ESV4J_jxanc&list=PL-x35fyliRwger2GwWLG4vigDRGCDyzCI
'''

# Docs: https://spark.apache.org/docs/latest/programming-guide.html
# Start Spark Python Shell with: bin/pyspark.cmd
# Browser GUI: http://localhost:4040/stages/

from pyspark import SparkContext, SparkConf
import glob
import re
import operator
from operator import add
from ast import literal_eval

folder = "c:/coding/Hadoop/Spark/"
mr_folder = "wuthering_heights_out2"

with open(folder + "wuthering_heights_out.txt", "wb") as outfile:
    content = open(folder + "wuthering_heights.txt", "rb").read()
    content = " ".join(re.compile("([\w][\w]*'?\w?)").findall(content)).lower()
    content = content.replace("' ", "") # Fix a couple of things...
    content = content.replace("'l l", "'ll")
    content = content.replace("'r e", "'re")
    content = content.replace("'v e", "'ve")
    outfile.write(content + "\n")

f = sc.textFile("file:///" + folder + "wuthering_heights_out.txt")
wc = f.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
wc.saveAsTextFile("file:///" + folder + mr_folder)

files = glob.glob(folder + mr_folder + "/part-*")
words = []
for f in files:
    for e, line in enumerate(open(f, "rb")):
        words.append(tuple(literal_eval(line.strip())))

words_sorted = sorted(words, key=operator.itemgetter(1), reverse=True)
print words_sorted[0:3]
print words_sorted[0][1] # Just get the frequency part

# Try some log parsing
f = sc.textFile("file:///" + "C:/coding/Hadoop/pig/MapReduceInputData/iis3.log")
errors = f.filter(lambda line: "139.116.15.40" in line).collect()
print errors[1:3]
errors = f.filter(lambda line: line.startswith("139.116.15.37,POSTEN")).collect()
f.filter(lambda x: x.contains("LMKBRUKER")).count()

errors = f.filter(lambda line: line.startswith("139.116.15.37,POSTEN"))
messages = errors.map(lambda s: s.split(',')[2]) # Get the third element in the tuplet
messages.cache()
messages.filter(lambda s: "7/28" in s).count()

messages = errors.map(lambda s: s.split(',')[2]).collect()

# --------------------------------------------------------------------------------------------
# Spark SQL:

# from pyspark.sql import SQLContext, Row
from pyspark.sql import *
sqlContext = SQLContext(sc)

messages = errors.map(lambda s: s.split(',')) # Get the first four elements in the tuplet
for m in messages[0][0:3]:
    print m # Get fields 0-3 of row 0

# Ex 1
lines = sc.textFile("file:///" + "C:/coding/Hadoop/pig/MapReduceInputData/iis3.log")
messages = lines.map(lambda l: l.split(","))
messages_subset = messages.map(lambda p: Row(ip=p[0], user=p[1], date=p[2], time=p[3]))    

# Ex 2
lines = sc.textFile("file:///" + "C:/coding/Hadoop/pig/MapReduceInputData/VH_Formtype.txt")
messages = lines.map(lambda l: l.split("\t"))
messages_subset = messages.map(lambda p: Row(formtypename=p[1]))    

# See example: http://spark.apache.org/docs/latest/sql-programming-guide.html 
schema_messages = sqlContext.inferSchema(messages_subset)

schemaString = "ip user date time"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
schemaPeople = sqlContext.applySchema(messages_subset, schema)

schema_messages.registerTempTable("messages_subset")

# Ex 1
data = sqlContext.sql("SELECT * FROM messages_subset") # Can then use RDD operations on the returned RDD
# #x 2
data = sqlContext.sql("""SELECT formtypename, count(formtypename) AS processed FROM
    messages_subset GROUP BY formtypename ORDER BY formtypename""")
data2 = data.map(lambda r: r).collect()
for d in data2: # An RDD(?) on Row objects. TODO: How to convert from Row?
    print d[0], d[1]
formtypes = {} # Add formtypes to a dictionary
for d in data2:
    formtypes[d[0]] = d[1]
print formtypes["CrossDocking"]

formTypes = data.map(lambda p: "FormTypeName: " + p.formtypename)
for formType in formTypes.collect():
  print formType

data3 = sqlContext.sql("""SELECT formtypename, count(formtypename) AS processed
  FROM messages_subset WHERE formtypename LIKE '%Bring%' GROUP BY formtypename""").map(lambda r: r).collect()
for d in data3:
    print d[0], d[1]

  
# Try to read a JSON file:
sqlContext = SQLContext(sc)
books = sqlContext.jsonFile("C:/coding/Hadoop/pig/MapReduceInputData/books.json")
books.printSchema()
books.registerTempTable("books")
books_result = sqlContext.sql("SELECT * FROM books")

# ----------------------------------------------------------------------------------------------------------------------------------------
# TODO: Try the Streaming API

# ----------------------------------------------------------------------------------------------------------------------------------------
# TODO: Try Data Frames (Spark 1.3)
# https://databricks.com/blog/2015/02/17/introducing-dataframes-in-spark-for-large-scale-data-science.html

sqlContext = SQLContext(sc)
df = sqlContext.jsonFile("C:/coding/hadoop/pig/MapReduceInputData/example2.json")
df.select("salary").show()

result = df[df["lastName"] == "Doe"].groupBy("firstName").sum("salary")
result.show()
result.printSchema()
df.select("firstName","lastName").show()
df.select("salary", df.salary * 10).show()
df.groupBy("lastName").count().show()
df.groupBy("lastName").sum().show()
df.groupBy("lastName").avg().show()

lines = sc.textFile("C:/coding/R/TestData/export_import.csv")
import pandas as pd
pandas_df = pd.read_csv("C:/coding/R/TestData/export_import.csv", header=1) # TODO: Check other py files for example
spark_df = sqlContext.createDataFrame(pandas_df)
spark_df.show()
spark_df.select("year","goods","services",goods-services).show()
spark_df.registerTempTable("spark_df")
sqlContext.sql("SELECT * FROM spark_df").show()

# Spark streaming:
# https://spark.apache.org/docs/latest/streaming-programming-guide.html
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# ----------------------------------------------------------------------------------------------------------------------------------------
# TODO: Try R, Cassandra, etc. integration (Spark 1.4, June '15)

# ----------------------------------------------------------------------------------------------------------------------------------------
# TODO:
# https://www.youtube.com/watch?v=FjhRkfAuU7I
# 1) Load tweets from Twitter (http://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.streaming.twitter.TwitterUtils$)
# 2) Convert the RDD of tweet data to an SQL RDD
# 3) Train a ML model with the MLLib on the SQL RDD
# 4) Load live Twitter data with the streaming API, and use that as test data for the ML model

