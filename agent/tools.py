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
# 1. DAU Tool
# =========================

def get_dau():

    connection = pymysql.connect(**DB_CONFIG)

    try:

        with connection.cursor() as cursor:

            sql = """
                  SELECT
                      stat_date,
                      active_user_count
                  FROM ads_daily_metrics
                  ORDER BY stat_date DESC
                      LIMIT 2 \
                  """

            cursor.execute(sql)

            result = cursor.fetchall()

            if len(result) == 2:

                today = result[0]["active_user_count"]
                yesterday = result[1]["active_user_count"]

                change = today - yesterday

                if yesterday != 0:

                    change_rate = round(
                        change / yesterday * 100,
                        2
                    )

                else:

                    change_rate = 0

                return {
                    "data": result,
                    "change": change,
                    "change_rate": change_rate
                }

            return {
                "data": result,
                "change": None,
                "change_rate": None
            }

    finally:

        connection.close()


# =========================
# 2. Course Hot Tool
# =========================

def get_course_hot():

    connection = pymysql.connect(**DB_CONFIG)

    try:

        with connection.cursor() as cursor:

            sql = """
                  SELECT
                      h.course_id,
                      c.course_name,
                      h.total_behavior_count,
                      h.view_count,
                      h.favorite_count,
                      h.start_learning_count,
                      h.finish_count
                  FROM ads_course_hot h
                           LEFT JOIN dim_course c
                                     ON h.course_id = c.course_id
                  ORDER BY h.total_behavior_count DESC
                      LIMIT 10 \
                  """

            cursor.execute(sql)

            return cursor.fetchall()

    finally:

        connection.close()


# =========================
# 3. Learning Tool
# =========================

def get_learning():

    connection = pymysql.connect(**DB_CONFIG)

    try:

        with connection.cursor() as cursor:

            sql = """
                  SELECT
                      DATE(event_time) AS stat_date,
                      behavior_type,
                      COUNT(*) AS behavior_count
                  FROM fact_user_behavior
                  WHERE DATE(event_time) >= (
                      SELECT DATE(MAX(event_time)) - INTERVAL 1 DAY
                      FROM fact_user_behavior
                      )
                  GROUP BY
                      DATE(event_time),
                      behavior_type
                  ORDER BY
                      stat_date DESC,
                      behavior_count DESC \
                  """

            cursor.execute(sql)

            result = cursor.fetchall()

            return result

    finally:

        connection.close()


# =========================
# 4. Data Quality Tool
# =========================

def get_quality():

    connection = pymysql.connect(**DB_CONFIG)

    try:

        with connection.cursor() as cursor:

            sql = """
                  SELECT
                      result_id,
                      rule_id,
                      table_name,
                      rule_name,
                      status,
                      error_count,
                      check_time,
                      check_batch_id
                  FROM data_quality_result
                  ORDER BY check_time DESC
                      LIMIT 10 \
                  """

            cursor.execute(sql)

            return cursor.fetchall()

    finally:

        connection.close()


# =========================
# 5. Tool 定义
# =========================

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_dau",
            "description": (
                "查询最近两天的每日活跃用户数 DAU，"
                "用于分析今天和昨天活跃用户数量变化。"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_course_hot",
            "description": (
                "查询课程热度排行，"
                "可以获取课程名称、总行为次数、浏览量、收藏数、"
                "开始学习人数和完成学习人数，"
                "用于分析哪些课程最热门。"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_learning",
            "description": (
                "查询最近两天的用户行为趋势，"
                "可以获取浏览、收藏、开始学习、完成学习等行为数量，"
                "用于分析用户活跃度变化以及 DAU 异常原因。"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_quality",
            "description": (
                "查询最近的数据质量检查结果，"
                "可以获取检查表、质量规则、检查状态、错误数量和检查时间，"
                "用于分析数据是否存在质量问题。"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "analyze_dau_anomaly",
            "description": (
                "分析今天 DAU 是否异常下降。"
                "当用户询问为什么活跃用户下降、DAU下降原因、"
                "活跃用户异常等问题时使用。"
                "该工具会综合分析 DAU、用户行为趋势和数据质量，"
                "给出异常原因、数据证据和处理建议。"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }

]