import json

from kafka import KafkaConsumer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "user_behavior"


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="datamind-test",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)


print("==============================")
print("DataMind Kafka Consumer")
print("==============================")
print("等待 Kafka 数据...")


for message in consumer:

    data = message.value

    print(
        f"收到数据："
        f"user={data['user_id']}, "
        f"course={data['course_id']}, "
        f"behavior={data['behavior_type']}, "
        f"time={data['event_time']}"
    )