升级spark
========

spark 2.2.1 => spark 2.4.7 => spark 3.0.1

(2020.09.24) spark cassandra connector 推出了 3.0.0 正式版，支持spark 3.0
为了项目今后长远考虑，打算采用spark 3.0.1，为此测试之

spark 3.0.1 使用的 scala 2.12

示例沿用hello_03，修改gradle中的版本配置

自适应执行
=========

spark 3.x的特色

https://blog.csdn.net/zyzzxycj/article/details/106469572

http://blog.madhukaraphatak.com/spark-aqe-part-1/  
http://blog.madhukaraphatak.com/spark-aqe-part-2/

https://blog.knoldus.com/adaptive-query-execution-aqe-in-spark-3-0/

```scala
val spark = SparkSession
    .builder
    .config("spark.cassandra.connection.host", CassSetting.host)
    .config("spark.cassandra.auth.username", CassSetting.username)
    .config("spark.cassandra.auth.password", CassSetting.password)
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .appName("查询cassandra数据")
    .getOrCreate()
```

安全提交
=======

https://stackoverflow.com/questions/47908699/authentication-for-spark-standalone-cluster

conf/spark-defaults.conf

spark.authenticate.secret      abc1234

代码增加配置参数  
.conf("spark.authenticate.secret", "abc1234")

DataFrame
=========

https://github.com/datastax/spark-cassandra-connector/blob/master/doc/14_data_frames.md

采用catalog方式读取cassandra

```scala
val spark = SparkSession
    .builder
    .config("spark.cassandra.connection.host", CassSetting.host)
    .config("spark.cassandra.auth.username", CassSetting.username)
    .config("spark.cassandra.auth.password", CassSetting.password)
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")
    .config("spark.sql.catalog.cass100", "com.datastax.spark.connector.datasource.CassandraCatalog")
    .appName("查询cassandra数据")
    .getOrCreate()

import spark.implicits._

// val df = spark
//     .read
//     .format("org.apache.spark.sql.cassandra")
//     .options(Map( "table" -> "brch_qry_dtl", "keyspace" -> "finance"))
//     .load

// df.createOrReplaceTempView("qry_dtl")

spark.sql("""
    select count(*) from cass100.finance.brch_qry_dtl
""").show()

spark.stop()
```

这种方式简化了读取的方式


启动spark
=========
spark 3.0.1

> ./sbin/start-master.sh -h localhost

> ./sbin/start-slave.sh spark://localhost:7077

读取cassandra
============

cassandra配置，参见hello_07

构建打包
=======

因aliyun的镜像，还没有spark cassandra connector 3.0.0，故repositories增加jcenter()  
若今后aliyun镜像中有，则可以去除jcenter()

gradle build
gradle shadowJar

提交计算
=======

> spark-submit --master spark://localhost:7077 --class brchqry.BrchQry ./brchqry/build/libs/brchqry-all.jar

hello_10 执行时间 16s ~ 17s  
hello_03 执行时间 14s ~ 15s

停止spark
=========

> ./sbin/stop-slave.sh

> ./sbin/stop-master.sh

spark shell
===========

> spark-shell --master spark://localhost:7077 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 --conf spark.cassandra.connection.host=localhost --conf spark.cassandra.auth.username=cassandra --conf spark.cassandra.auth.password=cassandra --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions

spark.conf.set(s"spark.sql.catalog.mycat", "com.datastax.spark.connector.datasource.CassandraCatalog")

spark.sql("select count(*) from mycat.finance.brch_qry_dtl").show()

spark.sql("select count(*) from mycat.finance.brch_qry_dtl").explain()
