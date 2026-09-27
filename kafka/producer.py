import json
import random
import time
from datetime import datetime

from kafka import KafkaProducer


# =========================
# 1. Kafka 配置
# =========================

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "user_behavior"


# =========================
# 2. 用户行为类型
# =========================

behavior_types = [
    "view",
    "favorite",
    "start_learning",
    "finish",
    "buy"
]


# =========================
# 3. 创建 Kafka Producer
# =========================

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,

    # Python 字典 → JSON 字符串 → bytes
    value_serializer=lambda value: json.dumps(
        value,
        ensure_ascii=False
    ).encode("utf-8")
)


print("=" * 50)
print("DataMind Kafka Producer 启动")
print(f"Kafka: {BOOTSTRAP_SERVERS}")
print(f"Topic: {TOPIC}")
print("=" * 50)


# =========================
# 4. 持续生成用户行为
# =========================

try:

    while True:

        # 生成一条用户行为数据
        data = {
            "user_id": f"U{random.randint(1, 1000):06d}",

            "course_id": f"C{random.randint(1, 100):05d}",

            "behavior_type": random.choice(
                behavior_types
            ),

            "event_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "duration": random.randint(
                0,
                3600
            )
        }

        # =========================
        # 发送 Kafka
        # =========================

        producer.send(
            TOPIC,
            value=data
        )

        producer.flush()

        # =========================
        # 控制台打印
        # =========================

        print(
            f"发送成功: "
            f"user={data['user_id']}, "
            f"course={data['course_id']}, "
            f"behavior={data['behavior_type']}, "
            f"time={data['event_time']}, "
            f"duration={data['duration']}"
        )

        # 每秒发送一条
        time.sleep(1)


except KeyboardInterrupt:

    print("\nProducer 已停止")


finally:

    producer.close()

    print("Kafka Producer 连接已关闭")
