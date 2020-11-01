package brchrpt

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import conf.{ Utils, CassSetting }

object BrchRpt {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder
      .config("spark.cassandra.connection.host", CassSetting.host)
      .config("spark.cassandra.auth.username", CassSetting.username)
      .config("spark.cassandra.auth.password", CassSetting.password)
      .appName("计算rpt_sum汇总")
      .getOrCreate()

    import spark.implicits._

    val df = spark
      .read
      .format("org.apache.spark.sql.cassandra")
      .options(Map("table" -> "brch_qry_dtl", "keyspace" -> "finance"))
      .load

    df.createOrReplaceTempView("qry_dtl")

    spark.sql("""
        select rpt_sum, sum(amt) from qry_dtl
        where tran_date='2019-11-27'
          and dr_cr_flag=1
        group by rpt_sum
    """).show()

    spark.stop()
  }
}