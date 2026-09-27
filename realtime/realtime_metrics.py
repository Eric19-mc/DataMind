import redis


# =========================
# 连接 Redis
# =========================

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# =========================
# 查询实时指标
# =========================

behaviors = [
    "view",
    "favorite",
    "start_learning",
    "finish",
    "buy"
]

print("=" * 40)
print("DataMind 实时用户行为指标")
print("=" * 40)

for behavior in behaviors:

    key = f"datamind:behavior:{behavior}"

    count = r.get(key)

    if count is None:
        count = 0

    print(f"{behavior:<15} {count}")

print("=" * 40)