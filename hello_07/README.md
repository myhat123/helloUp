cassandra
=========

版本： 3.11.8

xubuntu 中文环境下测试，需要调整 conf/cassandra-env.sh

system_memory_in_mb=`free -m | awk '/：/ {print $2;exit}'`

冒号有半角改为全角

cassandra集群的前提条件是，启用时间同步服务器，确保集群中各节点机的时间保持同步。

运行
===

> cassandra -f

命令行访问
========

> pyenv activate gopy3
> cqlsh -u cassandra -p cassandra localhost

cassandra配置
============

配置文件 conf/cassandra.yaml

常见配置选项

```yaml
# The name of the cluster. This is mainly used to prevent machines in
# one logical cluster from joining another.
cluster_name: 'Test Cluster'

# Authentication backend, implementing IAuthenticator; used to identify users
# Out of the box, Cassandra provides org.apache.cassandra.auth.{AllowAllAuthenticator,
# PasswordAuthenticator}.
#
# - AllowAllAuthenticator performs no checks - set it to disable authentication.
# - PasswordAuthenticator relies on username/password pairs to authenticate
#   users. It keeps usernames and hashed passwords in system_auth.roles table.
#   Please increase system_auth keyspace replication factor if you use this authenticator.
#   If using PasswordAuthenticator, CassandraRoleManager must also be used (see below)
authenticator: AllowAllAuthenticator

# any class that implements the SeedProvider interface and has a
# constructor that takes a Map<String, String> of parameters will do.
seed_provider:
    # Addresses of hosts that are deemed contact points. 
    # Cassandra nodes use this list of hosts to find each other and learn
    # the topology of the ring.  You must change this if you are running
    # multiple nodes!
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "127.0.0.1"


# Address or interface to bind to and tell other Cassandra nodes to connect to.
# You _must_ change this if you want multiple nodes to be able to communicate!
#
# Set listen_address OR listen_interface, not both.
#
# Leaving it blank leaves it up to InetAddress.getLocalHost(). This
# will always do the Right Thing _if_ the node is properly configured
# (hostname, name resolution, etc), and the Right Thing is to use the
# address associated with the hostname (it might not be).
#
# Setting listen_address to 0.0.0.0 is always wrong.
#
listen_address: localhost

# The address or interface to bind the Thrift RPC service and native transport
# server to.
#
# Set rpc_address OR rpc_interface, not both.
#
# Leaving rpc_address blank has the same effect as on listen_address
# (i.e. it will be based on the configured hostname of the node).
#
# Note that unlike listen_address, you can specify 0.0.0.0, but you must also
# set broadcast_rpc_address to a value other than 0.0.0.0.
#
# For security reasons, you should not expose this port to the internet.  Firewall it if needed.
rpc_address: localhost
```

安全认证配置
===========

配置文件 conf/cassandra.yaml

```yaml
authenticator: PaswordAuthenticator
```

默认的用户/口令 cassandra/cassandra

```sql
alter user cassandra with password '1234';
create user test with password '1234;
```

```cql
list users;
login test '1234'
```

可调的一致性
==========

写一致性级别
读一致性级别

性能调优
=======

cassandra权威指南（中文版）

P326 并发和线程

concurrent_reads     硬盘个数x16  
concurrent_writes    默认是32，可调整为应用服务器连接cassandra的线程数  
concurrent_counter_writes  
concurrent_materialized_view_writes  

P28 网络和超时

read_request_timeout_in_ms  
range_request_timeout_in_ms  
write_request_timeout_in_ms  
....

cross_node_timeout false  
启用ntp

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
