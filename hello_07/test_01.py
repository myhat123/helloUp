from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

auth_provider = PlainTextAuthProvider(
    username="cassandra",
    password="cassandra"
)

cluster = Cluster(['localhost'], auth_provider=auth_provider)
session = cluster.connect('finance')

rows = session.execute('SELECT acc, tran_date, rpt_sum, dr_cr_flag, amt FROM brch_qry_dtl')

for r in rows:
    # print(r.acc, r.tran_date, r.rpt_sum)
    print(r[0], r[1], r[2])