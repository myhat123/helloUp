from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

def main():
    conf = SparkConf()
    conf.set("spark.cassandra.connection.host", "localhost")
    conf.set("spark.cassandra.auth.username", "cassandra")
    conf.set("spark.cassandra.auth.password", "cassandra")

    spark = SparkSession \
        .builder \
        .config(conf=conf) \
        .appName("转换数据时间日期") \
        .getOrCreate()

    df = spark.sql("""
      SELECT explode(sequence(to_date('2018-01-01'), to_date('2018-03-01'), interval 1 month))
    """)

    df.show()

    df2 = spark.sql("""
      select cast(ts as Timestamp) from (
        SELECT explode(sequence(to_timestamp('2019-11-27 22:30:00'), to_timestamp('2019-11-28 22:30:00'), interval 30 minutes)) as ts
      ) t1
    """)

    df2.show()

    spark.stop()

if __name__ == "__main__":
    main()