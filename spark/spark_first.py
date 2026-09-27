from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# 1. 创建 SparkSession
spark = (
    SparkSession.builder
    .appName("DataMind-Spark-First")
    .master("local[*]")
    .getOrCreate()
)

print("==============================")
print("DataMind Spark 启动成功！")
print("==============================")


# 2. 读取用户数据
user_file = "../data-generator/data/user.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(user_file)
)


# 3. 查看数据结构
print("\n===== 数据结构 =====")
df.printSchema()


# 4. 查看前 10 条数据
print("\n===== 前10条数据 =====")
df.show(10, truncate=False)


# 5. 数据清洗
clean_df = (
    df
    .filter(col("user_id").isNotNull())
    .filter(col("username").isNotNull())
    .filter(col("age").between(18, 35))
)


# 6. 查看清洗后的数据量
print("\n===== 清洗结果 =====")
print(f"清洗前：{df.count()} 条")
print(f"清洗后：{clean_df.count()} 条")


# 7. 按省份统计用户数量
print("\n===== 各省份用户数量 =====")

(
    clean_df
    .groupBy("province")
    .count()
    .orderBy(col("count").desc())
    .show()
)


# 8. 停止 Spark
spark.stop()

print("==============================")
print("DataMind Spark 执行完成！")
print("==============================")