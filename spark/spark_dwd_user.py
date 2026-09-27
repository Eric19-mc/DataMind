from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim


# ==============================
# 1. 创建 SparkSession
# ==============================

spark = (
    SparkSession.builder
    .appName("DataMind-DWD-User")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("==============================")
print("DataMind Spark DWD 用户清洗")
print("==============================")


# ==============================
# 2. 找到 CSV 文件
# ==============================

project_dir = Path(__file__).resolve().parent.parent

user_file = (
        project_dir
        / "data-generator"
        / "data"
        / "user.csv"
)

print(f"用户数据文件：{user_file}")


# ==============================
# 3. 读取 ODS 数据
# ==============================

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(user_file))
)

print("\n===== ODS 用户数据结构 =====")

df.printSchema()


# ==============================
# 4. 查看原始数据
# ==============================

print("\n===== ODS 前10条数据 =====")

df.show(10, truncate=False)


# ==============================
# 5. 数据清洗
# ==============================

clean_df = (
    df
    .withColumn("user_id", trim(col("user_id")))
    .withColumn("username", trim(col("username")))
    .withColumn("province", trim(col("province")))
    .filter(col("user_id").isNotNull())
    .filter(col("user_id") != "")
    .filter(col("username").isNotNull())
    .filter(col("username") != "")
    .filter(col("age").between(18, 35))
)


# ==============================
# 6. 查看清洗结果
# ==============================

print("\n===== DWD 用户数据 =====")

clean_df.show(10, truncate=False)


# ==============================
# 7. 数据量统计
# ==============================

before_count = df.count()
after_count = clean_df.count()

print("\n===== 数据清洗统计 =====")

print(f"清洗前：{before_count} 条")
print(f"清洗后：{after_count} 条")
print(f"过滤掉：{before_count - after_count} 条")


# ==============================
# 8. 查看各省份用户数量
# ==============================

print("\n===== 各省份用户数量 =====")

(
    clean_df
    .groupBy("province")
    .count()
    .orderBy(col("count").desc())
    .show()
)


# ==============================
# 9. 停止 Spark
# ==============================

spark.stop()

print("==============================")
print("DWD 用户数据处理完成！")
print("==============================")