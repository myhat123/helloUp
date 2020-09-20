cassandra
=========

版本： 3.11.8

xubuntu 中文环境下测试，需要调整 conf/cassandra-env.sh

system_memory_in_mb=`free -m | awk '/：/ {print $2;exit}'`

冒号有半角改为全角

python读取cass
=============

https://github.com/datastax/python-driver

版本: 3.24.0

pip install cassandra-driver

```python
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
session = cluster.connect('finance')

rows = session.execute('SELECT acc, tran_date, rpt_sum, dr_cr_flag, amt FROM brch_qry_dtl')

for r in rows:
    # print(r.acc, r.tran_date, r.rpt_sum)
    print(r[0], r[1], r[2])
```
