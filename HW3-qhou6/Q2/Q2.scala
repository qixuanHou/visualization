// Databricks notebook source

case class edge (_c0: Integer, _c1: Integer, _c2: Integer)
val ds = spark.read.csv("/FileStore/tables/bitcoinotc.csv").withColumn("_c2", '_c2.cast("int")).withColumn("_c1", '_c1.cast("int")).withColumn("_c0", '_c0.cast("int")).as[edge]

val dsduplication = ds.dropDuplicates()

val dsfilter = dsduplication.filter("_c2 >= 5")

val group_0 = dsfilter.groupBy("_c0").sum("_c2")
val group_1 = dsfilter.groupBy("_c1").sum("_c2")

val names0 = Seq("node", "weighted-out-degree")
val names1 = Seq("node", "weighted-in-degree")

val group_00 = group_0.toDF(names0: _*)
val group_11 = group_1.toDF(names1: _*)
val joint = group_00.join(group_11, "node")

import org.apache.spark.sql.functions._

val finalTable = joint.withColumn("weighted-total-degree", (col("weighted-out-degree") + col("weighted-in-degree")))

val total = finalTable.agg(max("weighted-total-degree")).first().getLong(0)
val in = finalTable.agg(max("weighted-in-degree")).first().getLong(0)
val out = finalTable.agg(max("weighted-out-degree")).first().getLong(0)

val total_table = finalTable.filter(col("weighted-total-degree").equalTo(total)).agg(min("node")).first().getInt(0)
val in_table = finalTable.filter(col("weighted-in-degree").equalTo(in)).agg(min("node")).first().getInt(0)
val out_table = finalTable.filter(col("weighted-out-degree").equalTo(out)).agg(min("node")).first().getInt(0)


val someDF = Seq(
  (in_table, in, "i"),
  (out_table, out, "o"),
  (total_table, total, "t")
).toDF("v", "d", "c")

someDF.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true") .save("/FileStore/tables/test3.csv")
