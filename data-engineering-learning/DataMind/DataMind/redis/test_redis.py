import redis


client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# =========================
# 写入实时指标
# =========================

client.set("datamind:realtime:view", 100)
client.set("datamind:realtime:favorite", 35)
client.set("datamind:realtime:start_learning", 68)
client.set("datamind:realtime:finish", 42)


# =========================
# 读取实时指标
# =========================

view = client.get("datamind:realtime:view")
favorite = client.get("datamind:realtime:favorite")
start_learning = client.get("datamind:realtime:start_learning")
finish = client.get("datamind:realtime:finish")


print("==============================")
print("DataMind Redis Test")
print("==============================")

print("实时浏览：", view)
print("实时收藏：", favorite)
print("实时开始学习：", start_learning)
print("实时完成学习：", finish)