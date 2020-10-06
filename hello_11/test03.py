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

    df = spark.read \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="brch_qry_dtl", keyspace="finance") \
            .load()

    df.createOrReplaceTempView("qry_dtl")
    
    sqlDF = spark.sql("""
      select acc, rpt_sum, amt, 
        to_timestamp(timestamp1, 'yyyyMMddHHmmss') as ts
      from qry_dtl
      where tran_date='2019-11-27'
        and dr_cr_flag=1
        and acc='6042****4088'
    """)

    sqlDF.createOrReplaceTempView("qry_ts")

    df2 = spark.sql("""
      select acc, rpt_sum, amt, ts,
        window(ts, '30 minutes'),
        window(ts+INTERVAL 30 minutes, '30 minutes') as ts1
      from qry_ts
      where acc='6042****4088'
    """)

    df2.show()

    data = df2.collect()
    
    for x in data:
        print('ts1: {0}'.format(x['ts1']))

    spark.stop()

if __name__ == "__main__":
    main()