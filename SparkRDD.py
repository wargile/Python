# Doing some RDD stuff...
# https://regex101.com/#python

import datetime
import glob
import re
import operator
import sys
import os
from operator import add
from ast import literal_eval
from pyspark import SparkContext, SparkConf
from pyspark.sql import Row

# APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s?" (\d{3}) (\S+)'
LOG_PATTERN = '^(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)'

month_map = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,
    'Aug':8,  'Sep': 9, 'Oct':10, 'Nov': 11, 'Dec': 12}

def parse_IIS_time(s):
    """ Convert IIS datetime format into a Python datetime object
    Args:
        s (str): date and time in IIS datetime format
    Returns:
        datetime: datetime object
    """
    return datetime.datetime(int(s[1:4]),
                             month_map[s[6:7]],
                             int(s[9:10]),
                             int(s[12:13]),
                             int(s[15:16]),
                             int(s[18:19]))


def parseIISLogLine(logline):
    """ Parse a line in IIS Log format
    Args:
        logline (str): a line of text in the IIS Log format
    Returns:
        tuple: either a dictionary containing the parts of the IIS Log and 1,
               or the original invalid log line and 0
    """
    match = re.search(LOG_PATTERN, logline)

    if match is None:
        return (logline, 0)

    return (Row(
        date          = match.group(1), # use parse_IIS_time?
        time          = match.group(2), # use parse_IIS_time?
        endpoint      = match.group(3),
        verb          = match.group(4),
        url           = match.group(5),
        params        = match.group(6),
        port          = match.group(7),
        user_id       = match.group(8),
        client_ip     = match.group(9),
        browser_info  = match.group(10),
        response_code = match.group(11),
        unknown1      = match.group(12),
        unknown2      = match.group(13)
    ), 1)


baseDir = os.path.join('data')
inputPath = os.path.join('terje', 'iis.log')
logFile = os.path.join(baseDir, inputPath)
#print logFile

iis_log = sc.textFile(logFile).map(parseIISLogLine).cache()
#print iis_log

access_logs = (iis_log
               .filter(lambda s: s[1] == 1)
               .map(lambda s: s[0])
               .cache())

failed_logs = (iis_log
               .filter(lambda s: s[1] == 0)
               .map(lambda s: s[0]))
    
responseCodeToCount = (access_logs
                       .map(lambda log: (log.response_code, 1))
                       .reduceByKey(lambda a, b : a + b)
                       .cache())

responseCodeToCountList = responseCodeToCount.take(100)
print 'Found %d response codes' % len(responseCodeToCountList)
print 'Response Code Counts: %s' % responseCodeToCountList
