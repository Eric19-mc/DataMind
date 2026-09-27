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
    .appName("DataMind-ADS-DailyActive")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark ADS 每日活跃用户")
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


# ==============================
# 4. 数据清洗
# ==============================

clean_df = (
    df
    .filter(col("user_id").isNotNull())
    .filter(col("course_id").isNotNull())
    .filter(col("event_time").isNotNull())
)


# ==============================
# 5. 提取日期
# ==============================

clean_df = clean_df.withColumn(
    "event_date",
    to_date(col("event_time"))
)


# ==============================
# 6. 计算 DAU
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
# 7. 查看 ADS 数据
# ==============================

print("\n===== ADS 每日活跃用户 =====")

daily_active.show(50, truncate=False)


# ==============================
# 8. 创建 ADS 输出目录
# ==============================

ads_dir = project_dir / "data" / "ads"

ads_dir.mkdir(
    parents=True,
    exist_ok=True
)


# ==============================
# 9. 保存 ADS 数据
# ==============================

output_path = ads_dir / "daily_active"

(
    daily_active
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(output_path))
)


print("\nADS 数据保存位置：")
print(output_path)


# ==============================
# 10. 停止 Spark
# ==============================

spark.stop()

print("==============================")
print("ADS 每日活跃用户保存完成！")
print("==============================")