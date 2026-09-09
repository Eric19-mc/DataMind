import csv
from pathlib import Path
import pymysql


# =========================
# 1. 文件路径
# =========================
project_dir = Path(__file__).resolve().parent.parent

ads_dir = project_dir / "data" / "ads" / "user_learning"

csv_files = list(ads_dir.glob("part-*.csv"))

if not csv_files:
    raise FileNotFoundError("没有找到 Spark 生成的 ADS CSV 文件")

csv_file = csv_files[0]

print("读取文件：", csv_file)


# =========================
# 2. 连接 MySQL
# =========================
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="050622",
    database="datamind",
    charset="utf8mb4"
)

cursor = connection.cursor()


# =========================
# 3. 清空旧数据
# =========================
cursor.execute("TRUNCATE TABLE ads_user_learning")


# =========================
# 4. 读取 CSV
# =========================
with open(csv_file, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            """
            INSERT INTO ads_user_learning
            (
                user_id,
                total_learning_duration,
                avg_learning_duration,
                learning_behavior_count
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                row["user_id"],
                int(row["total_learning_duration"]),
                float(row["avg_learning_duration"]),
                int(row["learning_behavior_count"])
            )
        )


# =========================
# 5. 提交
# =========================
connection.commit()

cursor.close()
connection.close()

print("ADS 用户学习情况已经导入 MySQL！")