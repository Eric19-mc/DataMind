from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_date,
    countDistinct
)


# ==============================
# 1. 创建 SparkSession
# ==============================

spark = (
    SparkSession.builder
    .appName("DataMind-DWS-DailyActive")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark DWS 每日活跃用户")
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
# 3. 读取行为数据
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

print("\n===== 前10条用户行为 =====")

df.show(10, truncate=False)


# ==============================
# 5. 数据清洗
# ==============================

clean_df = (
    df
    .filter(col("user_id").isNotNull())
    .filter(col("course_id").isNotNull())
    .filter(col("event_time").isNotNull())
)


# ==============================
# 6. 提取行为日期
# ==============================

clean_df = clean_df.withColumn(
    "event_date",
    to_date(col("event_time"))
)


print("\n===== 增加 event_date 后 =====")

clean_df.show(10, truncate=False)


# ==============================
# 7. 计算每日活跃用户数
# ==============================

daily_active = (
    clean_df
    .groupBy("event_date")
    .agg(
        countDistinct("user_id").alias("daily_active_users")
    )
    .orderBy("event_date")
)


# ==============================
# 8. 查看 DWS 结果
# ==============================

print("\n===== DWS 每日活跃用户数 =====")

daily_active.show(50, truncate=False)


# ==============================
# 9. 停止 Spark
# ==============================

spark.stop()

print("==============================")
print("DWS 每日活跃用户计算完成！")
print("==============================")