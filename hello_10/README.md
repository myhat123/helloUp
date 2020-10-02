升级spark
========

spark 2.2.1 => spark 2.4.7 => spark 3.0.1

(2020.09.24) spark cassandra connector 推出了 3.0.0 正式版，支持spark 3.0
为了项目今后长远考虑，打算采用spark 3.0.1，为此测试之

spark 3.0.1 使用的 scala 2.12

示例沿用hello_03，修改gradle中的版本配置

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