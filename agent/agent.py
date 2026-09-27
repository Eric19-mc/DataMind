import pymysql


# =========================
# MySQL 配置
# =========================

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "050622",
    "database": "datamind",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}


# =========================
# Agent：意图识别
# =========================

def recognize_intent(question):

    question = question.lower()

    # DAU / 活跃用户
    if (
            "活跃用户" in question
            or "dau" in question
            or "活跃" in question
    ):
        return "dau"

    # 课程热度
    elif (
            "课程" in question
            or "热门" in question
            or "热度" in question
    ):
        return "course"

    # 用户学习
    elif (
            "学习" in question
            or "学习时长" in question
            or "用户行为" in question
    ):
        return "learning"

    # 数据质量
    elif (
            "数据质量" in question
            or "质量" in question
            or "脏数据" in question
    ):
        return "quality"

    return "unknown"


# =========================
# DAU 工具
# =========================

def get_dau(cursor):

    sql = """
          SELECT
              stat_date,
              active_user_count
          FROM ads_daily_metrics
          ORDER BY stat_date DESC
              LIMIT 2 \
          """

    cursor.execute(sql)

    return cursor.fetchall()


def analyze_dau(data):

    if len(data) < 2:
        return "暂无足够的 DAU 数据。"

    today = data[0]
    yesterday = data[1]

    today_value = today["active_user_count"]
    yesterday_value = yesterday["active_user_count"]

    change = today_value - yesterday_value

    if yesterday_value != 0:
        rate = change / yesterday_value * 100
    else:
        rate = 0

    if change < 0:

        return (
            f"今日活跃用户数为 {today_value}，"
            f"昨日为 {yesterday_value}，"
            f"下降 {abs(rate):.2f}%。"
        )

    elif change > 0:

        return (
            f"今日活跃用户数为 {today_value}，"
            f"昨日为 {yesterday_value}，"
            f"增长 {rate:.2f}%。"
        )

    return "今日活跃用户数与昨日基本持平。"


# =========================
# 课程热度工具
# =========================

def get_course_hot(cursor):

    sql = """
          SELECT
              course_id,
              total_behavior_count,
              view_count,
              favorite_count,
              start_learning_count,
              finish_count
          FROM ads_course_hot
          ORDER BY total_behavior_count DESC
              LIMIT 10 \
          """

    cursor.execute(sql)

    return cursor.fetchall()


def analyze_course(data):

    if not data:
        return "暂无课程热度数据。"

    result = "当前课程热度 TOP 5：\n"

    for i, row in enumerate(data[:5], 1):

        result += (
            f"{i}. 课程 {row['course_id']}："
            f"总行为 {row['total_behavior_count']} 次，"
            f"浏览 {row['view_count']} 次，"
            f"收藏 {row['favorite_count']} 次，"
            f"开始学习 {row['start_learning_count']} 次，"
            f"完成学习 {row['finish_count']} 次\n"
        )

    return result


# =========================
# 用户学习工具
# =========================

def get_learning(cursor):

    sql = """
          SELECT
              user_id,
              total_learning_duration,
              avg_learning_duration,
              learning_behavior_count
          FROM ads_user_learning
          ORDER BY total_learning_duration DESC
              LIMIT 10 \
          """

    cursor.execute(sql)

    return cursor.fetchall()


def analyze_learning(data):

    if not data:
        return "暂无用户学习数据。"

    result = "用户学习情况 TOP 5：\n"

    for i, row in enumerate(data[:5], 1):

        total_seconds = row["total_learning_duration"]

        hours = total_seconds / 3600

        result += (
            f"{i}. 用户 {row['user_id']}："
            f"总学习时长 {hours:.2f} 小时，"
            f"平均学习时长 {row['avg_learning_duration']:.2f} 秒，"
            f"学习行为 {row['learning_behavior_count']} 次\n"
        )

    return result


# =========================
# 数据质量工具
# =========================

def get_quality(cursor):

    sql = """
          SELECT
              rule_id,
              table_name,
              rule_name,
              rule_type,
              description,
              enabled,
              column_name,
              rule_value
          FROM data_quality_rule
          ORDER BY rule_id \
          """

    cursor.execute(sql)

    return cursor.fetchall()


def analyze_quality(data):

    if not data:
        return "暂无数据质量规则。"

    result = "当前数据质量规则：\n"

    for row in data:

        status = "启用" if row["enabled"] == 1 else "关闭"

        result += (
            f"- 规则 {row['rule_id']}："
            f"{row['rule_name']}，"
            f"表：{row['table_name']}，"
            f"字段：{row['column_name']}，"
            f"类型：{row['rule_type']}，"
            f"状态：{status}\n"
        )

    return result


# =========================
# Agent
# =========================

def main():

    print("=" * 60)
    print("        DataMind AI Agent")
    print("  输入 exit / quit 可以退出 Agent")
    print("=" * 60)

    # 建立一次数据库连接
    connection = pymysql.connect(**DB_CONFIG)

    try:

        while True:

            # =========================
            # 1. 获取用户问题
            # =========================

            question = input("\n请输入问题：").strip()

            # 空问题
            if not question:
                continue

            # 退出
            if question.lower() in ["exit", "quit"]:
                print("\nAgent 已退出。")
                break

            print("\n用户问题：", question)

            # =========================
            # 2. 意图识别
            # =========================

            intent = recognize_intent(question)

            print("识别意图：", intent)

            # =========================
            # 3. Agent 根据意图选择工具
            # =========================

            with connection.cursor() as cursor:

                if intent == "dau":

                    print("调用工具：DAU 查询")

                    data = get_dau(cursor)

                    answer = analyze_dau(data)

                elif intent == "course":

                    print("调用工具：课程热度查询")

                    data = get_course_hot(cursor)

                    answer = analyze_course(data)

                elif intent == "learning":

                    print("调用工具：用户学习查询")

                    data = get_learning(cursor)

                    answer = analyze_learning(data)

                elif intent == "quality":

                    print("调用工具：数据质量查询")

                    data = get_quality(cursor)

                    answer = analyze_quality(data)

                else:

                    answer = (
                        "暂时无法识别你的问题。\n"
                        "目前支持：\n"
                        "1. 活跃用户 / DAU\n"
                        "2. 课程热度\n"
                        "3. 用户学习\n"
                        "4. 数据质量"
                    )

            # =========================
            # 4. 输出结果
            # =========================

            print("\n========== Agent 分析结果 ==========")
            print(answer)
            print("====================================")


    finally:

        connection.close()


if __name__ == "__main__":
    main()