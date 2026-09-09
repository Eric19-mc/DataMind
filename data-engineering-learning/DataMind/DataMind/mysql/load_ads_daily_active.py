import csv
from pathlib import Path
import pymysql


# =========================
# 1. 文件路径
# =========================
project_dir = Path(__file__).resolve().parent.parent

ads_dir = project_dir / "data" / "ads" / "daily_active"

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
cursor.execute("TRUNCATE TABLE ads_daily_active")


# =========================
# 4. 读取 CSV
# =========================
with open(csv_file, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            """
            INSERT INTO ads_daily_active
                (event_date, daily_active_users)
            VALUES (%s, %s)
            """,
            (
                row["event_date"],
                int(row["daily_active_users"])
            )
        )


# =========================
# 5. 提交
# =========================
connection.commit()

cursor.close()
connection.close()

print("ADS 每日活跃用户已经导入 MySQL！")