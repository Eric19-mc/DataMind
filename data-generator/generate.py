import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# =========================
# 基础配置
# =========================

DATA_SIZE = 10000

OUTPUT_DIR = Path(__file__).parent / "data"

OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# 基础数据
# =========================

PROVINCES = [
    "广东",
    "湖南",
    "湖北",
    "浙江",
    "江苏",
    "四川",
    "山东",
    "河南",
    "北京",
    "上海"
]

COURSE_CATEGORIES = [
    "Python",
    "Java",
    "大数据",
    "人工智能",
    "数据库",
    "Web开发"
]

BEHAVIOR_TYPES = [
    "view",
    "favorite",
    "start_learning",
    "finish",
    "buy"
]


# =========================
# 生成用户数据
# =========================

def generate_users(count=1000):

    file_path = OUTPUT_DIR / "user.csv"

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.writer(file)

        writer.writerow([
            "user_id",
            "username",
            "gender",
            "age",
            "province",
            "register_time"
        ])

        for i in range(1, count + 1):

            user_id = f"U{i:06d}"

            username = f"user_{i}"

            gender = random.choice(["男", "女"])

            age = random.randint(18, 35)

            province = random.choice(PROVINCES)

            register_time = datetime.now() - timedelta(
                days=random.randint(0, 365)
            )

            writer.writerow([
                user_id,
                username,
                gender,
                age,
                province,
                register_time.strftime("%Y-%m-%d %H:%M:%S")
            ])

    print(f"用户数据生成完成：{file_path}")


# =========================
# 生成课程数据
# =========================

def generate_courses(count=100):

    file_path = OUTPUT_DIR / "course.csv"

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.writer(file)

        writer.writerow([
            "course_id",
            "course_name",
            "category",
            "teacher",
            "price"
        ])

        for i in range(1, count + 1):

            course_id = f"C{i:05d}"

            category = random.choice(COURSE_CATEGORIES)

            course_name = f"{category}课程{i}"

            teacher = f"teacher_{random.randint(1, 30)}"

            price = random.choice([
                0,
                29.9,
                49.9,
                99.9,
                199.9,
                299.9
            ])

            writer.writerow([
                course_id,
                course_name,
                category,
                teacher,
                price
            ])

    print(f"课程数据生成完成：{file_path}")


# =========================
# 生成用户行为数据
# =========================

def generate_behaviors(count=DATA_SIZE):

    file_path = OUTPUT_DIR / "user_behavior.csv"

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.writer(file)

        writer.writerow([
            "behavior_id",
            "user_id",
            "course_id",
            "behavior_type",
            "event_time",
            "duration"
        ])

        for i in range(1, count + 1):

            behavior_id = f"B{i:08d}"

            user_id = f"U{random.randint(1, 1000):06d}"

            course_id = f"C{random.randint(1, 100):05d}"

            behavior_type = random.choice(BEHAVIOR_TYPES)

            event_time = datetime.now() - timedelta(
                minutes=random.randint(0, 60 * 24 * 30)
            )

            duration = random.randint(0, 3600)

            writer.writerow([
                behavior_id,
                user_id,
                course_id,
                behavior_type,
                event_time.strftime("%Y-%m-%d %H:%M:%S"),
                duration
            ])

    print(f"用户行为数据生成完成：{file_path}")


# =========================
# 主程序
# =========================

if __name__ == "__main__":

    print("开始生成 DataMind 测试数据...")

    generate_users()

    generate_courses()

    generate_behaviors()

    print("================================")
    print("所有数据生成完成！")
    print("数据目录：", OUTPUT_DIR)
    print("================================")