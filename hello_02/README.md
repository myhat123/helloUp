启动spark
=========
spark 2.4.7

> ./sbin/start-master.sh -h localhost

> ./sbin/start-slave.sh spark://localhost:7077

写入cassandra
============

cassandra配置，参见hello_07

构建打包
=======

gradle build
gradle shadowJar

提交计算
=======

> spark-submit --master spark://localhost:7077 --class hello_02.FinTest ./build/libs/hello_02-all.jar