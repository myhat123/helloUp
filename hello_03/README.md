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