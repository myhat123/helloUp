spark本地运行
============

> ./sbin/start-master.sh -h localhost

> ./sbin/start-slave.sh spark://localhost:7077

pyspark
=======

spark 2.4.7 不支持python 3.8.x，而是支持python 3.5 ~ 3.7.x

> pyspark --packages com.datastax.spark:spark-cassandra-connector_2.11:2.5.1 --repositories https://maven.aliyun.com/nexus/content/groups/public/

执行spark job
============

> pyenv activate gopy3.6

> spark-submit --master spark://localhost:7077 --conf "spark.pyspark.driver.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --conf "spark.pyspark.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" pi.py

> spark-submit --master spark://localhost:7077 --conf "spark.pyspark.driver.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --conf "spark.pyspark.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --packages com.datastax.spark:spark-cassandra-connector_2.11:2.5.1,com.github.jnr:jnr-posix:3.1.1 test02.py

其中：jar包保存在 /home/hzg/.ivy2/jars

更改一个jar包名  

> cp com.github.jnr_jffi-1.3.0-native.jar com.github.jnr_jffi-1.3.0.jar

> spark-submit --master spark://localhost:7077 --conf "spark.pyspark.driver.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --conf "spark.pyspark.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --conf "spark.cassandra.connection.host=localhost" --conf "spark.cassandra.auth.username=cassandra" --conf "spark.cassandra.auth.password=cassandra" --packages com.datastax.spark:spark-cassandra-connector_2.11:2.5.1,com.github.jnr:jnr-posix:3.1.1 test01.py

切换python 3.7

> spark-submit --master spark://localhost:7077 --conf "spark.pyspark.driver.python=/home/hzg/.pyenv/versions/gopy3.7/bin/python" --conf "spark.pyspark.python=/home/hzg/.pyenv/versions/gopy3.7/bin/python" --conf "spark.cassandra.connection.host=localhost" --conf "spark.cassandra.auth.username=cassandra" --conf "spark.cassandra.auth.password=cassandra" --packages com.datastax.spark:spark-cassandra-connector_2.11:2.5.1,com.github.jnr:jnr-posix:3.1.1 test01.py

spark python api
================

http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameReader

options(**options)  
option(key, value)

获取行结果

http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Row

spark日期时间
============

> spark-submit --master spark://localhost:7077 --conf "spark.pyspark.driver.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --conf "spark.pyspark.python=/home/hzg/.pyenv/versions/gopy3.6/bin/python" --packages com.datastax.spark:spark-cassandra-connector_2.11:2.5.1,com.github.jnr:jnr-posix:3.1.1 test03.py