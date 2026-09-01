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


# =========================
# 质量检查函数
# =========================

def check_rule(cursor, rule):

    rule_id = rule["rule_id"]
    table_name = rule["table_name"]
    rule_name = rule["rule_name"]
    rule_type = rule["rule_type"]

    # ---------------------------------
    # 规则1：用户ID非空
    # ---------------------------------

    if rule_id == 1:

        sql = """
              SELECT COUNT(*)
              FROM dim_user
              WHERE user_id IS NULL
                 OR user_id = '' \
              """

    # ---------------------------------
    # 规则2：用户年龄范围
    # ---------------------------------

    elif rule_id == 2:

        sql = """
              SELECT COUNT(*)
              FROM dim_user
              WHERE age < 18
                 OR age > 35
                 OR age IS NULL \
              """

    # ---------------------------------
    # 规则3：课程价格非负
    # ---------------------------------

    elif rule_id == 3:

        sql = """
              SELECT COUNT(*)
              FROM dim_course
              WHERE price < 0
                 OR price IS NULL \
              """

    # ---------------------------------
    # 规则4：行为类型合法
    # ---------------------------------

    elif rule_id == 4:

        sql = """
              SELECT COUNT(*)
              FROM fact_user_behavior
              WHERE behavior_type NOT IN (
                                          'view',
                                          'favorite',
                                          'start_learning',
                                          'finish',
                                          'buy'
                  ) \
              """

    # ---------------------------------
    # 规则5：学习时长范围
    # ---------------------------------

    elif rule_id == 5:

        sql = """
              SELECT COUNT(*)
              FROM fact_user_behavior
              WHERE duration < 0
                 OR duration > 3600
                 OR duration IS NULL \
              """

    # ---------------------------------
    # 规则6：用户引用完整
    # ---------------------------------

    elif rule_id == 6:

        sql = """
              SELECT COUNT(*)
              FROM fact_user_behavior b
                       LEFT JOIN dim_user u
                                 ON b.user_id = u.user_id
              WHERE u.user_id IS NULL \
              """

    # ---------------------------------
    # 规则7：课程引用完整
    # ---------------------------------

    elif rule_id == 7:

        sql = """
              SELECT COUNT(*)
              FROM fact_user_behavior b
                       LEFT JOIN dim_course c
                                 ON b.course_id = c.course_id
              WHERE c.course_id IS NULL \
              """

    else:

        return None

    cursor.execute(sql)

    error_count = cursor.fetchone()[0]

    status = "PASS" if error_count == 0 else "FAIL"

    return {
        "rule_id": rule_id,
        "table_name": table_name,
        "rule_name": rule_name,
        "status": status,
        "error_count": error_count
    }


# =========================
# 主程序
# =========================

try:

    with connection.cursor(
            pymysql.cursors.DictCursor
    ) as cursor:

        # =========================
        # 读取启用的质量规则
        # =========================

        cursor.execute("""
                       SELECT
                           rule_id,
                           table_name,
                           rule_name,
                           rule_type
                       FROM data_quality_rule
                       WHERE enabled = 1
                       ORDER BY rule_id
                       """)

        rules = cursor.fetchall()


        # =========================
        # 执行规则
        # =========================

        results = []

        for rule in rules:

            result = check_rule(cursor, rule)

            if result is not None:

                results.append(result)


        # =========================
        # 输出报告
        # =========================

        print()
        print("========================================")
        print("       DataMind Quality Engine")
        print("========================================")

        print()

        for result in results:

            print(
                f"规则 {result['rule_id']} | "
                f"{result['table_name']} | "
                f"{result['rule_name']} | "
                f"{result['status']} | "
                f"异常数量：{result['error_count']}"
            )


        # =========================
        # 计算评分
        # =========================

        total_rules = len(results)

        passed_rules = sum(
            1
            for result in results
            if result["status"] == "PASS"
        )

        if total_rules == 0:

            score = 0

        else:

            score = passed_rules / total_rules * 100


        print()
        print("========================================")
        print(f"规则通过率：{score:.2f}%")
        print("========================================")


except Exception as e:

    print("数据质量引擎运行失败：")
    print(e)


finally:

    connection.close()

    print()
    print("MySQL 连接已关闭。")

