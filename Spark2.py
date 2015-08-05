# http://stackoverflow.com/questions/8644741/novice-python-regex-pull-strings-between-a-tags-using-regex

# -- In sandbox, get HTML data from Hortonworks page on Wikipedia:
# wget http://wikipedia.org/wiki/Hortonworks
# -- Put it on HDFS:
# hadoop fs -put ~/Hortonworks /user/guest/Hortonworks
# -- Start pyspark:
# pyspark

myLines = sc.textFile('hdfs://sandbox.hortonworks.com/user/guest/Hortonworks')
myLines_filtered = myLines.filter( lambda x: len(x) > 0 )
# -- Find all <img> tags
imageLines = myLines_filtered.filter(lambda a: re.compile('\<\i\m\g').findall(a))
# TODO: Get the text between tags
# http://stackoverflow.com/questions/8644741/novice-python-regex-pull-strings-between-a-tags-using-regex
