读取cassandra
============

cassandra配置，参见hello_07

构建打包
=======

gradle build
gradle shadowJar

gradle :brchrpt:build
gradle :brchrpt:shadowJar

提交计算
=======

> spark-submit --master spark://localhost:7077 --class brchqry.BrchQry ./brchqry/build/libs/brchqry-all.jar

> spark-submit --master spark://localhost:7077 --total-executor-cores 2 --executor-memory 512M --class brchrpt.BrchRpt ./brchrpt/build/libs/brchrpt-all.jar

spark-shell
============

> spark-shell --master spark://localhost:7077 --packages com.datastax.spark:spark-cassandra-connector_2.11:2.5.1 

packages 保存在  
Ivy Default Cache set to: /home/hzg/.ivy2/cache  
The jars for the packages stored in: /home/hzg/.ivy2/jars

spark.conf.set("spark.cassandra.connection.host", "localhost")
spark.conf.set("spark.cassandra.auth.username", "cassandra")
spark.conf.set("spark.cassandra.auth.password", "cassandra")

val df = spark.read.format("org.apache.spark.sql.cassandra").options(Map( "table" -> "brch_qry_dtl", "keyspace" -> "finance")).load