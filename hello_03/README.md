读取cassandra
============

cassandra配置，参见hello_07

构建打包
=======

gradle build
gradle shadowJar

提交计算
=======

> spark-submit --master spark://localhost:7077 --class brchqry.BrchQry ./brchqry/build/libs/brchqry-all.jar