from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    avg,
    count
)


# ==============================
# 1. 创建 SparkSession
# ==============================

spark = (
    SparkSession.builder
    .appName("DataMind-DWS-UserLearning")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark DWS 用户学习时长")
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
# 4. 查看数据
# ==============================

print("\n===== 前10条数据 =====")

df.show(10, truncate=False)


# ==============================
# 5. 数据清洗
# ==============================

clean_df = (
    df
    .filter(col("user_id").isNotNull())
    .filter(col("course_id").isNotNull())
    .filter(col("behavior_type").isNotNull())
    .filter(col("duration").isNotNull())
    .filter(col("duration") >= 0)
)


# ==============================
# 6. 只保留学习行为
# ==============================

learning_df = (
    clean_df
    .filter(
        col("behavior_type").isin(
            "start_learning",
            "finish"
        )
    )
)


print("\n===== 学习行为数据 =====")

learning_df.show(10, truncate=False)


# ==============================
# 7. 计算用户学习时长
# ==============================

user_learning = (
    learning_df
    .groupBy("user_id")
    .agg(
        sum("duration").alias("total_learning_duration"),
        avg("duration").alias("avg_learning_duration"),
        count("*").alias("learning_behavior_count")
    )
    .orderBy(
        col("total_learning_duration").desc()
    )
)


# ==============================
# 8. 查看结果
# ==============================

print("\n===== DWS 用户学习时长 =====")

user_learning.show(20, truncate=False)


# ==============================
# 9. 停止 Spark
# ==============================

spark.stop()

print("==============================")
print("DWS 用户学习时长计算完成！")
print("==============================")