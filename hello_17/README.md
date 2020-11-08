启动spark
=========
spark 2.4.7

> ./sbin/start-master.sh -h localhost

> ./sbin/start-slave.sh spark://localhost:7077

写入postgresql
=============

postgresql配置，参见hello_04

构建打包
=======

gradle build
gradle shadowJar

提交计算
=======

> spark-submit --master spark://localhost:7077 --class hello_17.FinTest ./build/libs/hello_17-all.jar