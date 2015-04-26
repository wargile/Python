# Cassandra test
# pip install cassandra-driver
# http://datastax.github.io/python-driver/getting_started.html

from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect('Weather_data') # NOTE: "" not needed here as in a CQL statement
session.execute('USE "Weather_data"') # NOTE: But here we need 'em in the CQL statement
rows = session.execute('SELECT event_time, temperature FROM temperature WHERE weatherstation_id=\'1234ABCD\';')

for user_row in rows:
    print user_row.event_time, user_row.temperature # Nice...
