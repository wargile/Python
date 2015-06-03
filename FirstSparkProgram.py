"""
FirstSparkProgram.py
Run with:
/usr/hdp/2.2.4.2-2/spark/bin/spark-submit --master local[4] FirstSparkProgram.py
(NOTE: local[n] param specifies number of partitions for result file (and node processing?))
"""

from pyspark import SparkContext

if __name__ == "__main__":
    #sc = SparkContext("local", "FirstSparkProgram")
    sc = SparkContext(appName="FirstSparkProgram")

    f = sc.textFile("hdfs://0.0.0.0:8020/user/hue/iis3.log")
    # f = sc.textFile("hdfs://sandbox.hortonworks.com:8020/tmp/littlelog.csv")
    my_data = f.filter(lambda line: "139.116.15.40" in line).cache().collect()
    # print my_data[1:5]
    my_data = f.filter(lambda line: line.startswith("139.116.15.37,POSTEN\Johansen")).collect()
    split_data = my_data[0].split(',')

    for x in split_data:
        print x

    # NOTE: my_data is now a list, convert to RDD and store on HDFS
    # Use coalesce(1, True) for creating a single output partition (with SMALL datasets!)
    sc.parallelize(my_data).coalesce(1, True).saveAsTextFile("hdfs://0.0.0.0:8020/user/terje/Processed_IIS3")
    print "All done!"
