import pymysql


# =========================
# MySQL 配置
# =========================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "050622"
DB_NAME = "datamind"


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

print("========================================")
print("       DataMind 数据质量检测报告")
print("========================================")


# =========================
# 数据质量检查
# =========================

try:

    with connection.cursor() as cursor:

        # ---------------------------------
        # 1. dim_user：user_id 为空
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM dim_user
                       WHERE user_id IS NULL
                          OR user_id = ''
                       """)

        user_id_error = cursor.fetchone()[0]


        # ---------------------------------
        # 2. dim_user：年龄异常
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM dim_user
                       WHERE age < 18
                          OR age > 35
                          OR age IS NULL
                       """)

        age_error = cursor.fetchone()[0]


        # ---------------------------------
        # 3. dim_course：价格异常
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM dim_course
                       WHERE price < 0
                          OR price IS NULL
                       """)

        price_error = cursor.fetchone()[0]


        # ---------------------------------
        # 4. fact_user_behavior：行为类型异常
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM fact_user_behavior
                       WHERE behavior_type NOT IN (
                                                   'view',
                                                   'favorite',
                                                   'start_learning',
                                                   'finish',
                                                   'buy'
                           )
                       """)

        behavior_type_error = cursor.fetchone()[0]


        # ---------------------------------
        # 5. fact_user_behavior：学习时长异常
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM fact_user_behavior
                       WHERE duration < 0
                          OR duration > 3600
                          OR duration IS NULL
                       """)

        duration_error = cursor.fetchone()[0]


        # ---------------------------------
        # 6. fact_user_behavior：用户不存在
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM fact_user_behavior b
                                LEFT JOIN dim_user u
                                          ON b.user_id = u.user_id
                       WHERE u.user_id IS NULL
                       """)

        user_reference_error = cursor.fetchone()[0]


        # ---------------------------------
        # 7. fact_user_behavior：课程不存在
        # ---------------------------------

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM fact_user_behavior b
                                LEFT JOIN dim_course c
                                          ON b.course_id = c.course_id
                       WHERE c.course_id IS NULL
                       """)

        course_reference_error = cursor.fetchone()[0]


    # =========================
    # 输出结果
    # =========================

    print()

    print("[dim_user]")
    print(
        f"user_id为空       {'PASS' if user_id_error == 0 else 'FAIL'}    {user_id_error}"
    )

    print(
        f"年龄异常           {'PASS' if age_error == 0 else 'FAIL'}    {age_error}"
    )

    print()

    print("[dim_course]")
    print(
        f"课程价格异常       {'PASS' if price_error == 0 else 'FAIL'}    {price_error}"
    )

    print()

    print("[fact_user_behavior]")
    print(
        f"行为类型非法       {'PASS' if behavior_type_error == 0 else 'FAIL'}    {behavior_type_error}"
    )

    print(
        f"学习时长异常       {'PASS' if duration_error == 0 else 'FAIL'}    {duration_error}"
    )

    print(
        f"用户ID不存在        {'PASS' if user_reference_error == 0 else 'FAIL'}    {user_reference_error}"
    )

    print(
        f"课程ID不存在        {'PASS' if course_reference_error == 0 else 'FAIL'}    {course_reference_error}"
    )


    # =========================
    # 计算质量评分
    # =========================

    errors = (
            user_id_error
            + age_error
            + price_error
            + behavior_type_error
            + duration_error
            + user_reference_error
            + course_reference_error
    )

    if errors == 0:
        score = 100
    else:
        score = max(0, 100 - errors)


    print()
    print("========================================")
    print(f"数据质量评分：{score}%")
    print("========================================")


except Exception as e:

    print()
    print("数据质量检测失败：")
    print(e)


finally:

    connection.close()