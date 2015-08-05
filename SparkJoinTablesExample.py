
# coding: utf-8

# In[1]:

"""
Some Spark SQL...
"""

import os
#import sys
import glob
import re
import math
import matplotlib.pyplot as plt # http://matplotlib.org/users/customizing.html
#import operator
from operator import add
#from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
from pyspark.sql.types import *

get_ipython().magic(u'matplotlib inline')

spark_home = os.environ.get('SPARK_HOME', None)
print('SPARK initialized OK! The SPARK home directory is: ' + spark_home)


# In[4]:

# https://spark.apache.org/docs/latest/sql-programming-guide.html
train_set = sc.textFile('C:/coding/Kaggle/CaterpillarTubePricing/Data/data/competition_data/train_set_no_header.csv')
tube = sc.textFile('C:/coding/Kaggle/CaterpillarTubePricing/Data/data/competition_data/tube_no_header.csv')

train_set = sc.textFile('hdfs://sandbox.hortonworks.com:8020/user/terje/train_set_no_header.csv')
tube = sc.textFile('hdfs://sandbox.hortonworks.com:8020/user/terje/tube_no_header.csv')

lines = tube.map(lambda p: p.split(',')).collect()[0:10]
for line in lines:
    print line

elements = tube.flatMap(lambda p: p.split(',')).map(lambda p: (p, 1)).reduceByKey(lambda a, b: a + b)
elements.takeOrdered(20, key=lambda x: -x[1])
 
# Skip header line first (works OK in shell):
# header_line = train_set.map(lambda x: x).first()
# train_set2 = train_set.filter(lambda x: x.startswith('TA-'))
train_set_data = (train_set.map(lambda l: l.split(",")).map(lambda p: [p[0],p[1],p[2],int(p[3]),int(p[4]),p[5],
                                                                       int(p[6]),float(p[7])]))
tube_data = (tube.map(lambda l: l.split(",")).map(lambda p: [p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],
                                                            p[10],p[11],p[12],p[13],p[14],p[15]]))

tube_header = 'tube_assembly_id,material_id,diameter,wall,length,num_bends,bend_radius,' + \
              'end_a_1x,end_a_2x,end_x_1x,end_x_2x,end_a,end_x,num_boss,num_bracket,other'

schema = (StructType([
    StructField("tube_assembly_id", StringType(), True),
    StructField("supplier", StringType(), True),
    StructField("quote_date", StringType(), True),
    StructField("annual_usage", IntegerType(), True),
    StructField("min_order_quantity", IntegerType(), True),
    StructField("bracket_pricing", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("cost", FloatType(), True)
]))

fields = [StructField(field_name, StringType(), True) for field_name in tube_header.split(',')]
tube_schema = StructType(fields)


# In[6]:

tube_data.filter(lambda p: float(p[2]) > 155.0).collect()

train_set_data_df = sqlContext.createDataFrame(train_set_data, schema)
# train_set_data_df.show()
tube_data_df = sqlContext.createDataFrame(tube_data, tube_schema)

# Register the DataFrame as a table
train_set_data_df.registerTempTable('train_set')
tube_data_df.registerTempTable('tube')

# SQL can be run over DataFrames that have been registered as a table
result = sqlContext.sql('SELECT * FROM train_set WHERE cost > 33.33 ORDER BY cost DESC')
result.show()
# The results of SQL queries are RDDs and support all the normal RDD operations


# In[14]:

# https://github.com/databricks/spark-csv
# csv_file = 'C:/coding/Kaggle/CaterpillarTubePricing/Data/data/competition_data/train_set.csv'
# df = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load(csv_file)
# df.show()
# df.select('year', 'model').write.format('com.databricks.spark.csv').save('newdata.csv')


# In[ ]:

# TODO:
result = sqlContext.sql("SELECT * FROM train_set t1 JOIN tube t2 ON t1.tube_assembly_id=t2.tube_assembly_id").collect


# In[ ]:



