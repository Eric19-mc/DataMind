from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    when
)


# ==============================
# 1. 创建 SparkSession
# ==============================

spark = (
    SparkSession.builder
    .appName("DataMind-DWS-CourseHot")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark DWS 课程热度统计")
print("==============================")


# ==============================
# 2. 找到用户行为数据
# ==============================

project_dir = Path(__file__).resolve().parent.parent

behavior_file = (
        project_dir
        / "data-generator"
        / "data"
        / "user_behavior.csv"
)

print(f"行为数据文件：{behavior_file}")


# ==============================
# 3. 读取数据
# ==============================

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(behavior_file))
)

print("\n===== 用户行为数据结构 =====")

df.printSchema()


# ==============================
# 4. 查看原始数据
# ==============================

print("\n===== 前10条数据 =====")

df.show(10, truncate=False)


# ==============================
# 5. 基础数据清洗
# ==============================

clean_df = (
    df
    .filter(col("user_id").isNotNull())
    .filter(col("course_id").isNotNull())
    .filter(col("behavior_type").isNotNull())
)


# ==============================
# 6. 统计课程热度
# ==============================

course_hot = (
    clean_df
    .groupBy("course_id")
    .agg(
        count("*").alias("total_behavior_count"),

        count(
            when(col("behavior_type") == "view", True)
        ).alias("view_count"),

        count(
            when(col("behavior_type") == "favorite", True)
        ).alias("favorite_count"),

        count(
            when(col("behavior_type") == "start_learning", True)
        ).alias("start_learning_count"),

        count(
            when(col("behavior_type") == "finish", True)
        ).alias("finish_count")
    )
    .orderBy(
        col("total_behavior_count").desc()
    )
)


# ==============================
# 7. 查看结果
# ==============================

print("\n===== DWS 课程热度统计 =====")

course_hot.show(20, truncate=False)


# ==============================
# 8. 停止 Spark
# ==============================

spark.stop()

print("==============================")
print("DWS 课程热度统计完成！")
print("==============================")