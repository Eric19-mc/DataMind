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
# 数据库连接
# =========================

connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)


# =========================
# 生成检查 SQL
# =========================

def build_sql(rule):

    table_name = rule["table_name"]
    column_name = rule["column_name"]
    rule_type = rule["rule_type"]
    rule_value = rule["rule_value"]


    # =========================
    # NOT_NULL
    # =========================

    if rule_type == "NOT_NULL":

        sql = f"""
            SELECT COUNT(*) AS error_count
            FROM `{table_name}`
            WHERE `{column_name}` IS NULL
               OR `{column_name}` = ''
        """

        return sql


    # =========================
    # RANGE
    # =========================

    elif rule_type == "RANGE":

        values = rule_value.split(",")

        min_value = values[0]
        max_value = values[1] if len(values) > 1 else None

        if max_value is not None:

            sql = f"""
                SELECT COUNT(*) AS error_count
                FROM `{table_name}`
                WHERE `{column_name}` < {min_value}
                   OR `{column_name}` > {max_value}
                   OR `{column_name}` IS NULL
            """

        else:

            sql = f"""
                SELECT COUNT(*) AS error_count
                FROM `{table_name}`
                WHERE `{column_name}` < {min_value}
                   OR `{column_name}` IS NULL
            """

        return sql


    # =========================
    # ENUM
    # =========================

    elif rule_type == "ENUM":

        values = rule_value.split(",")

        value_list = ",".join(
            f"'{value}'"
            for value in values
        )

        sql = f"""
            SELECT COUNT(*) AS error_count
            FROM `{table_name}`
            WHERE `{column_name}` NOT IN ({value_list})
               OR `{column_name}` IS NULL
        """

        return sql


    # =========================
    # REFERENCE
    # =========================

    elif rule_type == "REFERENCE":

        reference_table, reference_column = rule_value.split(".")

        sql = f"""
            SELECT COUNT(*) AS error_count
            FROM `{table_name}` t
            LEFT JOIN `{reference_table}` r
                ON t.`{column_name}` = r.`{reference_column}`
            WHERE r.`{reference_column}` IS NULL
        """

        return sql


    return None


# =========================
# 主程序
# =========================

try:

    with connection.cursor() as cursor:

        # =========================
        # 读取启用规则
        # =========================

        cursor.execute("""
                       SELECT
                           rule_id,
                           table_name,
                           rule_name,
                           column_name,
                           rule_type,
                           rule_value
                       FROM data_quality_rule
                       WHERE enabled = 1
                       ORDER BY rule_id
                       """)

        rules = cursor.fetchall()


        results = []


        # =========================
        # 执行所有规则
        # =========================

        for rule in rules:

            sql = build_sql(rule)

            if sql is None:

                continue

            cursor.execute(sql)

            result = cursor.fetchone()

            error_count = result["error_count"]

            status = (
                "PASS"
                if error_count == 0
                else "FAIL"
            )

            results.append({
                "rule_id": rule["rule_id"],
                "table_name": rule["table_name"],
                "rule_name": rule["rule_name"],
                "status": status,
                "error_count": error_count
            })

            cursor.execute("""
                           INSERT INTO data_quality_result
                           (
                               rule_id,
                               table_name,
                               rule_name,
                               status,
                               error_count,
                               check_time
                           )
                           VALUES
                               (%s, %s, %s, %s, %s, NOW())
                           """, (
                               rule["rule_id"],
                               rule["table_name"],
                               rule["rule_name"],
                               status,
                               error_count
                           ))


        connection.commit()

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
        # 计算通过率
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

    print()
    print("数据质量引擎运行失败：")
    print(e)


finally:

    connection.close()

    print()
    print("MySQL 连接已关闭。")