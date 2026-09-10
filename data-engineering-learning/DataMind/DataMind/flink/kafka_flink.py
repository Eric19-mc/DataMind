import json
import redis

from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor


# =========================
# 课程热度统计
# =========================

class CourseHeatProcessFunction(KeyedProcessFunction):

    def open(self, runtime_context):

        descriptor = ValueStateDescriptor(
            "course_heat",
            Types.INT()
        )

        self.count_state = runtime_context.get_state(
            descriptor
        )

        # 连接 Redis / Memurai
        self.redis = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    def process_element(self, value, ctx):

        user_id = value[0]
        course_id = value[1]
        behavior_type = value[2]

        # 获取当前课程热度
        current_count = self.count_state.value()

        if current_count is None:
            current_count = 0

        current_count += 1

        # 更新 Flink 状态
        self.count_state.update(current_count)

        # 写入 Redis
        redis_key = f"datamind:course:heat:{course_id}"

        self.redis.set(
            redis_key,
            current_count
        )

        # 输出
        yield (
            user_id,
            course_id,
            behavior_type,
            current_count
        )


def main():

    # =========================
    # 1. Flink 环境
    # =========================

    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    # =========================
    # 2. Kafka Connector
    # =========================

    env.add_jars(
        "file:///D:/flink/lib/flink-connector-kafka.jar",
        "file:///D:/flink/lib/kafka-clients.jar"
    )

    # =========================
    # 3. Kafka Source
    # =========================

    source = KafkaSource.builder() \
        .set_bootstrap_servers("localhost:9092") \
        .set_topics("user_behavior") \
        .set_group_id("datamind-course-heat") \
        .set_value_only_deserializer(
        SimpleStringSchema()
    ) \
        .build()

    # =========================
    # 4. Kafka → Flink
    # =========================

    stream = env.from_source(
        source,
        watermark_strategy=WatermarkStrategy.no_watermarks(),
        source_name="Kafka User Behavior"
    )

    # =========================
    # 5. JSON 解析
    # =========================

    def parse_json(value):

        try:

            data = json.loads(value)

            return (
                data.get("user_id"),
                data.get("course_id"),
                data.get("behavior_type")
            )

        except Exception:

            return (
                "unknown",
                "unknown",
                "unknown"
            )

    result = stream.map(
        parse_json,
        output_type=Types.TUPLE([
            Types.STRING(),
            Types.STRING(),
            Types.STRING()
        ])
    )

    # =========================
    # 6. 按 course_id 分组
    # =========================

    keyed_stream = result.key_by(
        lambda x: x[1],
        key_type=Types.STRING()
    )

    # =========================
    # 7. 实时课程热度
    # =========================

    counted_stream = keyed_stream.process(
        CourseHeatProcessFunction(),
        output_type=Types.TUPLE([
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
            Types.INT()
        ])
    )

    # =========================
    # 8. 打印结果
    # =========================

    counted_stream.print()

    # =========================
    # 9. 启动
    # =========================

    env.execute(
        "DataMind Course Realtime Heat"
    )


if __name__ == "__main__":
    main()

