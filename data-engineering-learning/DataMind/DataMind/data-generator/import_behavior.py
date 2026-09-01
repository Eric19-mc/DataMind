import csv
import pymysql
from pathlib import Path


# =========================
# MySQL 配置
# =========================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "050622"
DB_NAME = "datamind"


# =========================
# CSV 文件
# =========================

BASE_DIR = Path(__file__).parent
BEHAVIOR_FILE = BASE_DIR / "data" / "user_behavior.csv"


# =========================
# 连接 MySQL
# =========================

connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset="utf8mb4"
)

print("MySQL 连接成功！")


# =========================
# 导入用户行为数据
# =========================

try:

    with connection.cursor() as cursor:

        with open(
                BEHAVIOR_FILE,
                "r",
                encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            sql = """
                  INSERT INTO fact_user_behavior
                  (
                      behavior_id,
                      user_id,
                      course_id,
                      behavior_type,
                      event_time,
                      duration
                  )
                  VALUES
                      (
                          %s, %s, %s, %s, %s, %s
                      ) \
                  """

            count = 0

            for row in reader:

                cursor.execute(
                    sql,
                    (
                        row["behavior_id"],
                        row["user_id"],
                        row["course_id"],
                        row["behavior_type"],
                        row["event_time"],
                        row["duration"]
                    )
                )

                count += 1

    connection.commit()

    print(f"成功导入 {count} 条用户行为数据！")


except Exception as e:

    connection.rollback()

    print("数据导入失败：")
    print(e)


finally:

    connection.close()

    print("MySQL 连接已关闭。")