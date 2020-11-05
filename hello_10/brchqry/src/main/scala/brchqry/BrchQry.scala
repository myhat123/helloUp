package brchqry

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import conf.{Utils, CassSetting}

object BrchQry {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder
      .config("spark.cassandra.connection.host", CassSetting.host)
      .config("spark.cassandra.auth.username", CassSetting.username)
      .config("spark.cassandra.auth.password", CassSetting.password)
      .config("spark.sql.adaptive.enabled", "true")
      .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
      .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")
      .config("spark.cassandra.input.fetch.sizeInRows", "10000")
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
