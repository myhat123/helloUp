/*
 * This Scala source file was generated by the Gradle 'init' task.
 */
package hello_15

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object FinTest {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder
      .appName("写入postgresql数据")
      .getOrCreate()
    
    import spark.implicits._

    val df = spark.read.options(Map("inferSchema"->"true","delimiter"->",","header"->"true"))
                        .csv("file:///home/hzg/work/helloUp/data-files/data.csv")
    df.createOrReplaceTempView("qry_dtl")

    df.write
      .format("jdbc")
      .option("url", "jdbc:postgresql://localhost/jr?user=jxyz&password=1234")
      .option("driver", "org.postgresql.Driver")
      .option("dbtable", "brch_qry_dtl")
      .option("truncate", "true")
      .mode("overwrite")
      .save()

    spark.stop()
  }
}