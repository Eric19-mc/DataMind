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
    .appName("DataMind-ADS-CourseHot")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark ADS 热门课程")
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
    .filter(col("behavior_type").isNotNull())
)


# ==============================
# 5. 计算课程热度
# ==============================

course_hot = (
    clean_df
    .groupBy("course_id")
    .agg(
        count("*").alias("total_behavior_count"),

        count(
            when(
                col("behavior_type") == "view",
                True
            )
        ).alias("view_count"),

        count(
            when(
                col("behavior_type") == "favorite",
                True
            )
        ).alias("favorite_count"),

        count(
            when(
                col("behavior_type") == "start_learning",
                True
            )
        ).alias("start_learning_count"),

        count(
            when(
                col("behavior_type") == "finish",
                True
            )
        ).alias("finish_count")
    )
    .orderBy(
        col("total_behavior_count").desc()
    )
)


# ==============================
# 6. 查看 ADS 数据
# ==============================

print("\n===== ADS 热门课程 =====")

course_hot.show(
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

output_path = ads_dir / "course_hot"

(
    course_hot
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
print("ADS 热门课程保存完成！")
print("==============================")