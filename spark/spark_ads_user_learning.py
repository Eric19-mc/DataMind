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
    .appName("DataMind-ADS-UserLearning")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark ADS 用户学习情况")
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
    .filter(col("duration").isNotNull())
)


# ==============================
# 5. 计算用户学习情况
# ==============================

user_learning = (
    clean_df
    .groupBy("user_id")
    .agg(
        sum("duration").alias(
            "total_learning_duration"
        ),

        avg("duration").alias(
            "avg_learning_duration"
        ),

        count("*").alias(
            "learning_behavior_count"
        )
    )
    .orderBy(
        col("total_learning_duration").desc()
    )
)


# ==============================
# 6. 查看 ADS 数据
# ==============================

print("\n===== ADS 用户学习情况 =====")

user_learning.show(
    50,
    truncate=False
)


# ==============================
# 7. 创建 ADS 输出目录
# ==============================

ads_dir = project_dir / "data" / "ads"

ads_dir.mkdir(
    parents=True,
    exist_ok=True
)


# ==============================
# 8. 保存 ADS 数据
# ==============================

output_path = ads_dir / "user_learning"

(
    user_learning
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(str(output_path))
)


print("\nADS 数据保存位置：")
print(output_path)


# ==============================
# 9. 停止 Spark
# ==============================

spark.stop()

print("==============================")
print("ADS 用户学习情况保存完成！")
print("==============================")