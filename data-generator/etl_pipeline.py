import pymysql
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "050622",
    "database": "datamind",
    "charset": "utf8mb4"
}


def get_connection():
    return pymysql.connect(
        **DB_CONFIG
    )

def generate_batch_id():
    return datetime.now().strftime("batch_%Y%m%d_%H%M%S")

def write_job_log(
        connection,
        batch_id,
        job_name,
        start_time,
        end_time,
        status,
        message,
        row_count
):
    with connection.cursor() as cursor:
        cursor.execute("""
                       INSERT INTO etl_job_log
                       (
                           batch_id,
                           job_name,
                           start_time,
                           end_time,
                           status,
                           message,
                           row_count
                       )
                       VALUES
                           (
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s
                           )
                       """, (
                           batch_id,
                           job_name,
                           start_time,
                           end_time,
                           status,
                           message,
                           row_count
                       ))

def load_dwd_user(connection, batch_id):

    job_name = "DWD_USER"
    start_time = datetime.now()

    print("开始处理 DWD 用户数据...")

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                           TRUNCATE TABLE dwd_user
                           """)

            cursor.execute("""
                           INSERT INTO dwd_user
                           (
                               user_id,
                               username,
                               gender,
                               age,
                               province,
                               register_time
                           )
                           SELECT
                               TRIM(user_id),
                               TRIM(username),
                               gender,
                               age,
                               TRIM(province),
                               register_time
                           FROM ods_user
                           WHERE user_id IS NOT NULL
                             AND user_id <> ''
                             AND username IS NOT NULL
                             AND username <> ''
                             AND age BETWEEN 18 AND 35
                           """)

            row_count = cursor.rowcount

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "SUCCESS",
            "DWD 用户数据处理成功",
            row_count
        )

        print(
            f"DWD 用户数据处理完成：{row_count} 条"
        )

    except Exception as e:

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "FAILED",
            str(e),
            0
        )

        raise

def load_dwd_course(connection, batch_id):

    job_name = "DWD_COURSE"
    start_time = datetime.now()

    print("开始处理 DWD 课程数据...")

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                           TRUNCATE TABLE dwd_course
                           """)

            cursor.execute("""
                           INSERT INTO dwd_course
                           (
                               course_id,
                               course_name,
                               category,
                               teacher,
                               price
                           )
                           SELECT
                               TRIM(course_id),
                               TRIM(course_name),
                               TRIM(category),
                               TRIM(teacher),
                               price
                           FROM ods_course
                           WHERE course_id IS NOT NULL
                             AND course_id <> ''
                             AND course_name IS NOT NULL
                             AND course_name <> ''
                             AND price >= 0
                           """)

            row_count = cursor.rowcount

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "SUCCESS",
            "DWD 课程数据处理成功",
            row_count
        )

        print(
            f"DWD 课程数据处理完成：{row_count} 条"
        )

    except Exception as e:

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "FAILED",
            str(e),
            0
        )

        raise

def load_dwd_behavior(connection, batch_id):

    job_name = "DWD_BEHAVIOR"
    start_time = datetime.now()

    print("开始处理 DWD 用户行为数据...")

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                           TRUNCATE TABLE dwd_user_behavior
                           """)

            cursor.execute("""
                           INSERT INTO dwd_user_behavior
                           (
                               behavior_id,
                               user_id,
                               course_id,
                               behavior_type,
                               event_time,
                               duration
                           )
                           SELECT
                               TRIM(b.behavior_id),
                               TRIM(b.user_id),
                               TRIM(b.course_id),
                               TRIM(b.behavior_type),
                               b.event_time,
                               b.duration
                           FROM ods_user_behavior b

                                    INNER JOIN dwd_user u
                                               ON TRIM(b.user_id) = u.user_id

                                    INNER JOIN dwd_course c
                                               ON TRIM(b.course_id) = c.course_id

                           WHERE b.behavior_id IS NOT NULL
                             AND b.behavior_id <> ''

                             AND b.behavior_type IN (
                                                     'view',
                                                     'favorite',
                                                     'start_learning',
                                                     'finish',
                                                     'buy'
                               )

                             AND b.duration BETWEEN 0 AND 3600
                           """)

            row_count = cursor.rowcount

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "SUCCESS",
            "DWD 行为数据处理成功",
            row_count
        )

        print(
            f"DWD 行为数据处理完成：{row_count} 条"
        )

    except Exception as e:

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "FAILED",
            str(e),
            0
        )

        raise

def load_dws_daily_behavior(connection, batch_id):

    job_name = "DWS_DAILY_BEHAVIOR"
    start_time = datetime.now()

    print("开始计算 DWS 每日行为指标...")

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                           TRUNCATE TABLE dws_daily_behavior
                           """)

            cursor.execute("""
                           INSERT INTO dws_daily_behavior
                           (
                               stat_date,
                               view_count,
                               favorite_count,
                               start_learning_count,
                               finish_count,
                               buy_count,
                               active_user_count,
                               study_user_count
                           )
                           SELECT
                               DATE(event_time),

                               SUM(
                               CASE
                               WHEN behavior_type = 'view'
                               THEN 1
                               ELSE 0
                               END
                               ),

                               SUM(
                               CASE
                               WHEN behavior_type = 'favorite'
                               THEN 1
                               ELSE 0
                               END
                               ),

                               SUM(
                               CASE
                               WHEN behavior_type = 'start_learning'
                               THEN 1
                               ELSE 0
                               END
                               ),

                               SUM(
                               CASE
                               WHEN behavior_type = 'finish'
                               THEN 1
                               ELSE 0
                               END
                               ),

                               SUM(
                               CASE
                               WHEN behavior_type = 'buy'
                               THEN 1
                               ELSE 0
                               END
                               ),

                               COUNT(DISTINCT user_id),

                               COUNT(
                               DISTINCT CASE
                               WHEN behavior_type IN (
                               'start_learning',
                               'finish'
                               )
                               THEN user_id
                               END
                               )

                           FROM dwd_user_behavior

                           GROUP BY DATE(event_time)
                           """)

            row_count = cursor.rowcount

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "SUCCESS",
            "DWS 每日指标计算成功",
            row_count
        )

        print(
            f"DWS 每日指标计算完成：{row_count} 条"
        )

    except Exception as e:

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "FAILED",
            str(e),
            0
        )

        raise

def load_ads_daily_metrics(connection, batch_id):

    job_name = "ADS_DAILY_METRICS"
    start_time = datetime.now()

    print("开始生成 ADS 每日指标...")

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                           TRUNCATE TABLE ads_daily_metrics
                           """)

            cursor.execute("""
                           INSERT INTO ads_daily_metrics
                           (
                               stat_date,
                               active_user_count,
                               study_user_count,
                               view_count,
                               favorite_count,
                               start_learning_count,
                               finish_count,
                               buy_count,
                               conversion_rate
                           )
                           SELECT
                               stat_date,
                               active_user_count,
                               study_user_count,
                               view_count,
                               favorite_count,
                               start_learning_count,
                               finish_count,
                               buy_count,

                               CASE
                                   WHEN start_learning_count = 0
                                       THEN 0
                                   ELSE ROUND(
                                           buy_count /
                                           start_learning_count,
                                           4
                                        )
                                   END

                           FROM dws_daily_behavior
                           """)

            row_count = cursor.rowcount

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "SUCCESS",
            "ADS 每日指标生成成功",
            row_count
        )

        print(
            f"ADS 每日指标生成完成：{row_count} 条"
        )

    except Exception as e:

        end_time = datetime.now()

        write_job_log(
            connection,
            batch_id,
            job_name,
            start_time,
            end_time,
            "FAILED",
            str(e),
            0
        )

        raise

def main():

    print("==============================")
    print("DataMind ETL Pipeline")
    print("==============================")

    connection = get_connection()

    try:
        print("MySQL 连接成功！")

        batch_id = generate_batch_id()

        print(f"本次 ETL 批次：{batch_id}")

        # DWD
        load_dwd_user(connection, batch_id)
        load_dwd_course(connection, batch_id)
        load_dwd_behavior(connection, batch_id)

        # DWS
        load_dws_daily_behavior(connection, batch_id)

        # ADS
        load_ads_daily_metrics(connection, batch_id)

        connection.commit()

        print("==============================")
        print("ETL 执行成功！")
        print("==============================")

    except Exception as e:

        connection.rollback()

        print("==============================")
        print("ETL 执行失败！")
        print("==============================")
        print(e)

    finally:

        connection.close()

        print("MySQL 连接已关闭。")


if __name__ == "__main__":
    main()