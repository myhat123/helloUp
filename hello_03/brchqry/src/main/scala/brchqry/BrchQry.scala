package brchqry

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import conf.Utils

object BrchQry {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder
      .appName("查询cassandra数据")
      .getOrCreate()

    import spark.implicits._

    val df = spark
        .read
        .format("org.apache.spark.sql.cassandra")
        .options(Map( "table" -> "brch_qry_dtl", "keyspace" -> "finance"))
        .load

    df.createOrReplaceTempView("qry_dtl")

    spark.sql("""
        select count(*) from qry_dtl
    """).show()

    spark.stop()
  }
}
