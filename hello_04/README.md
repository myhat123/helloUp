postgresql
==========

参考资料

https://wiki.postgresql.org/wiki/Apt

1. 导入 the repository key from https://www.postgresql.org/media/keys/ACCC4CF8.asc

```sh
sudo apt-get install curl ca-certificates gnupg
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
2. 创建 /etc/apt/sources.list.d/pgdg.list

ubuntu 18.04, 加入如下

```sh
deb http://apt.postgresql.org/pub/repos/apt bionic-pgdg main
```

或者

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

3. 安装postgresql-12

```sh
sudo apt-get update
sudo apt-get install postgresql-12
```

配置文件目录  /etc/postgresql/12/main  
pg_hba.conf  postgresql.conf

4. 安装pgbouncer

参考资料

https://www.cnblogs.com/lottu/p/9640604.html

轻量级的缓冲池 pgbouncer 1.14.0

```sh
sudo apt-get install pgbouncer
```

配置文件  
/etc/pgbouncer/pgbouncer.ini  
/etc/pgbouncer/userlist.txt

pgbouncer目前支持三种连接池模型。分别是session, transaction和statment三个级别。

1. session 会话级链接。只有与当客户端的会话结束时，pgbouncer才会收回已分配的链接
2. transaction 事务级连接。当事务完成后，pgbouncer会回收已分配的链接。也就是说客户端只是在事务中才能独占此链接，非事务的对数据库的请求是没有独享的链接的。
3. statement 语句级链接。任何对数据库的请求完成后，pgbouncer都会回收链接。此种模式下，客户端不能使用事务，否则会造成数据的不一致。

创建数据库
=========

sudo su
su - postgres
createuser -P -e jxyz (密码: 1234)
createdb -O jxyz -E utf8 jr

psql -h localhost -U jxyz -d jr
create schema finance

psql -h localhost -U jxyz -d jr < ../data-files/schema.sql

psql中切换模式  
show search_path;
set search_path to finance;

ALTER ROLE jxyz SET search_path = finance;

python psycopg2安装
==================

pip install psycopg2-binary

加载测试数据
==========

连接字符串  
https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING

直连数据库的字符串 => postgresql://jxyz:1234@localhost/jr

pyenv activate gopy3

python sqldb.py

配置pgbouncer
============

/etc/pgbouncer/pgbouncer.ini  

```ini
[databases]
db_jr = host=localhost port=5432 dbname=jr

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
```

/etc/pgbouncer/userlist.txt

使用apt-get安装后，有 /usr/share/pgbouncer/mkauth.py

sudo su
su - postgres
psql

postgres=# select usename, passwd from pg_shadow order by 1;
 usename  |               passwd                
----------+-------------------------------------
 jxyz     | md5a92ce60d478cd50a0797b73b83df53de
 postgres | 
(2 行记录)

sudo /etc/init.d/pgbouncer restart

通过pgbouncer连接数据库，默认是20个连接  
psql -h localhost -p 6432 -U jxyz -d db_jr

postgresql.conf
===============

参考资料:   
PostgreSQL11生产环境常用参数配置参考 https://blog.csdn.net/kouryoushine/article/details/88852153
配置参考: 服务器配置：8核cpu 16GB 内存。

1. max_connections = 300
决定数据库的最大并发连接数。

参考值：不超过物理内存(GB)*50。

2. shared_buffers =4GB
设置数据库服务器将使用的共享内存缓冲区量。默认通常是 128 兆字节（128MB）

参考值： 1/4 主机内存

3. work_mem = 16MB
写到临时磁盘文件之前被内部排序操作和哈希表使用的内存量。
排序、去重、归并需要排序，再生成临时变落入磁盘之前，会在内存中占用一部分空间。同一个时刻，可能有很多排序的工作都会按此参数分配内存，所以这个值不能太大。
如果要使用语句中有较大的排序操作，可以在会话级别设置该参数，set work_men = ‘2GB’,提高执行速度。
参考值：# 1/4 主机内存 / 256 (假设256个并发同时使用work_mem)

4. maintenance_work_mem =1GB
指定在维护性操作（例如VACUUM、CREATE INDEX和ALTER TABLE ADD FOREIGNKEY）中使用的最大的内存量。这样的操作并不频繁，所以可以比work_men大很多。

参考值
内存的1/4除以autovacuum_max_workers数量。
系统内存超过32G时，建议设置为1GB。超过64GB时，建议设置为2GB。超过128GB时，建议设置为4GB。主要作用是改进清理和恢复数据库转储的性能，设定一个autovacuum_max_workers匹配值就好。

5. effective_cache_size
设置规划器对一个单一查询可用的有效磁盘缓冲区尺寸的假设
更高的数值会使得索引扫描更可能被使用，更低的数值会使
得顺序扫描更可能被使用。它只用于估计的目的

参考值：内存一半

并行参数配置
==========

参考资料:  

https://blog.csdn.net/ctypyb2002/article/details/84062392  
https://developer.aliyun.com/article/670732  
http://www.postgres.cn/docs/11/sql-createindex.html  
https://www.cybertec-postgresql.com/en/postgresql-parallel-create-index-for-better-performance/

postgresql 11 并行进程调整为两类:
第一类是并行查询，其并行度由 max_parallel_workers_per_gather 控制
第二类是维护命令(例如 CREATE INDEX)，其并行度由 max_parallel_maintenance_workers 控制。

下面三个参数主要控制并发工作者数量，对于性能有不小影响。

1. max_worker_processes = 32
系统能够支持的后台进程的最大数量,很多processes都需要获取的根源，所以尽可能保证充足的线程数量。

2. max_parallel_workers = 4
并行工作者数量，从max_worker_processes获取，所以不能大于后者。

参考值：cpu-4

3. max_parallel_workers_per_gather = 4
每个查询并行工作者数量，不能大于上面两个

参考值：cpu-4

4. max_parallel_maintenance_workers
设置维护命令(例如 CREATE INDEX) 允许的最大并行进程数，默认值为2。

系统管理
=======

参考资料: https://www.postgresqltutorial.com/postgresql-administration/

显示数据表

```sql
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
```

显示数据库

```sql
SELECT datname FROM pg_database;
```

显示数据表结构

```sql
SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'brch_qry_dtl';
```

显示模式

```sql
SELECT * 
FROM pg_catalog.pg_namespace
ORDER BY nspname;
```

显示数据表大小

```sql
select pg_relation_size('brch_qry_dtl');
```

```sql
SELECT pg_size_pretty (pg_relation_size('brch_qry_dtl'));
```

```sql
SELECT
    pg_size_pretty (
        pg_total_relation_size ('brch_qry_dtl')
    );
```

显示数据库大小

```sql
SELECT
    pg_size_pretty (
        pg_database_size ('jr')
    );
```

```sql
SELECT
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
    FROM pg_database;
```

```sql
SELECT
    pg_size_pretty (pg_indexes_size('brch_qry_dtl'));
```