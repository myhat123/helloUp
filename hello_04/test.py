import sqldb

x = sqldb.SQLDB(sqldb.CONN_STR)

# for y in x.read_data():
#     print(y)

x.read_data()