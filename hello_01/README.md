参考资料

https://github.com/datastax/SparkBuildExamples/tree/master/scala/gradle/oss  
https://github.com/DataStax-Examples/SparkBuildExamples/tree/master/scala/gradle/oss

spark cassandra connector的文档中提到了这个示例参考
我是从这里才了解到gradle作为scala, spark的构建工具

具体要求的版本号，可以到 https://mvnrepository.com/ 查找

参考资料

https://guides.gradle.org/building-scala-libraries/

gradle 6.4

> gradle init --type scala-library

build.gradle 文件

spark文档
=========

Spark runs on Java 8, Python 2.7+/3.4+ and R 3.5+. For the Scala API, Spark 2.4.7 uses Scala 2.12. You will need to use a compatible Scala version (2.12.x).

其实仍然是使用scala 2.11.x，见spark-2.4.7目录下的jar，全是scala 2.11的版本库

http://spark.apache.org/downloads.html

Note that, Spark 2.x is pre-built with Scala 2.11 except version 2.4.2, which is pre-built with Scala 2.12. Spark 3.0+ is pre-built with Scala 2.12.

启动spark
=========
spark 2.4.7

> ./sbin/start-master.sh -h localhost

> ./sbin/start-slave.sh spark://localhost:7077

spark自带管理器
http://localhost:8080/

交互式环境
========

> ./bin/spark-shell --master spark://localhost:7077

构建打包
=======

gradle build
gradle shadowJar

提交计算
=======

> spark-submit --master spark://localhost:7077 --class hello_01.SparkPi ./build/libs/hello_01-all.jar

> spark-submit --master spark://localhost:7077 --deploy-mode client --total-executor-cores 2 --executor-memory 512M --class hello_01.SparkPi ./build/libs/hello_01-all.jar

spark参数优化
============

在实战项目中，spark 2.4.7增加了参数来优化计算

spark-defaults.conf

spark.default.parallelism          120  
spark.sql.shuffle.partitions       120  
spark.speculation                  true  

spark.shuffle.file.buffer          64kb  
spark.reducer.maxSizeInFlight      96mb    

计算速度提升较多
