import json
import random
import time
from datetime import datetime

from kafka import KafkaProducer


# =========================
# Kafka 配置
# =========================

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "user_behavior"


# =========================
# 创建 Producer
# =========================

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(
        value,
        ensure_ascii=False
    ).encode("utf-8")
)


# =========================
# 模拟行为
# =========================

behavior_types = [
    "view",
    "favorite",
    "start_learning",
    "finish"
]


print("==============================")
print("DataMind Kafka Producer")
print("==============================")
print("开始发送实时用户行为...")


try:
    while True:

        data = {
            "user_id": f"U{random.randint(1, 1000):06d}",
            "course_id": f"C{random.randint(1, 100):05d}",
            "behavior_type": random.choice(behavior_types),
            "event_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "duration": random.randint(0, 3600)
        }

        producer.send(
            TOPIC,
            value=data
        )

        producer.flush()

        print("发送数据：", data)

        time.sleep(1)


except KeyboardInterrupt:

    print("\n停止 Producer")

finally:

    producer.close()