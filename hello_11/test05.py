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
    """)

    sqlDF.createOrReplaceTempView("qry_ts")

    df2 = spark.sql("""
      select acc, rpt_sum, amt, ts, ts.start as ts1
      from (
        select acc, rpt_sum, amt, 
            window(ts+INTERVAL 30 minutes, '30 minutes') as ts
        from qry_ts
      ) t1
    """)

    df2.createOrReplaceTempView("qry_data")

    df3 = spark.sql("""
      select cast(ts as Timestamp) as ts1 from (
        SELECT explode(sequence(to_timestamp('2019-11-26 22:30:00'), to_timestamp('2019-11-27 22:30:00'), interval 30 minutes)) as ts
      ) t1
    """)

    df3.createOrReplaceTempView("timeseries")

    df4 = spark.sql("""
      select t1.ts1, sum(coalesce(t2.amt, 0)) as amt
      from timeseries t1
      left join qry_data t2
      on (t1.ts1=t2.ts1)
      group by t1.ts1
      order by t1.ts1
    """)
    
    data = df4.collect()
    
    for x in data:
        print('时间: {0}, 金额: {1}'.format(x['ts1'], x['amt']))

    spark.stop()

if __name__ == "__main__":
    main()