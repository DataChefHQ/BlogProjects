package simple

import org.apache.spark.sql.{SaveMode, SparkSession}
import org.apache.spark.SparkConf
import org.apache.spark.sql.functions._

object SimpleSpark {
  private val parquetFmt = "parquet"
  protected lazy val spark: SparkSession =
    SparkSession.builder
      .enableHiveSupport()
      .config("spark.hadoop.fs.s3a.multiobjectdelete.enable", "false")
      .config("spark.hadoop.fs.s3a.fast.upload", "true")
      .config(new SparkConf)
      .getOrCreate()

  object Columns {
    val date = "date"
  }

  def main(args: Array[String]): Unit = {
    val arguments = Arguments(args)

    val df = spark.read
      .option("multiline", true)
      .json(arguments.sourcePath)
      .withColumn(Columns.date, current_date)

    df.repartition(col(Columns.date))
      .write
      .mode(SaveMode.Overwrite)
      .partitionBy(Columns.date)
      .format(parquetFmt)
      .option("path", arguments.destPath)
      .save()
  }
}
