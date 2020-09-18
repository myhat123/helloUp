CREATE KEYSPACE finance
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
