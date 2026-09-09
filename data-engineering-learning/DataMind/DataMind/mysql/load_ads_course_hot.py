import csv
from pathlib import Path
import pymysql


# =========================
# 1. 文件路径
# =========================
project_dir = Path(__file__).resolve().parent.parent

ads_dir = project_dir / "data" / "ads" / "course_hot"

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
cursor.execute("TRUNCATE TABLE ads_course_hot")


# =========================
# 4. 读取 CSV
# =========================
with open(csv_file, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            """
            INSERT INTO ads_course_hot
            (
                course_id,
                total_behavior_count,
                view_count,
                favorite_count,
                start_learning_count,
                finish_count
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                row["course_id"],
                int(row["total_behavior_count"]),
                int(row["view_count"]),
                int(row["favorite_count"]),
                int(row["start_learning_count"]),
                int(row["finish_count"])
            )
        )


# =========================
# 5. 提交
# =========================
connection.commit()

cursor.close()
connection.close()

print("ADS 热门课程已经导入 MySQL！")