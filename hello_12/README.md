启动spark
=========
spark 2.4.7

> ./sbin/start-master.sh -h localhost

> ./sbin/start-slave.sh spark://localhost:7077

写入clickhouse
============

clickhouse参见helloCH系列

```scala
 df2.write
    .format("jdbc")
    .mode("append")
    .option("driver", "ru.yandex.clickhouse.ClickHouseDriver")
    .option("url", "jdbc:clickhouse://localhost:8123/finance")
    .option("user", "hzg")
    .option("password", "1234")
    .option("dbtable", "brch_qry_dtl")
    .option("batchsize", 10000)
    .option("isolationLevel", "NONE")
    .save
```

使用clickhouse官方提供的jdbc
只能append，采用overwrite，会直接删除表，重建表时会生成engine的错误信息，应该是兼容的问题

虽然不完美，但可以使用这种方式

clickhouse native jdbc，这个包2.4版本，正在集成spark的接口，还没有最终定版，需等待。

构建打包
=======

gradle build
gradle shadowJar

提交计算
=======

>  spark-submit --master spark://localhost:7077 --class hello_12.FinTest ./build/libs/hello_12-all.jar