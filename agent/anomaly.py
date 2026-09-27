# =========================
# DataMind 异常原因分析引擎
# =========================

from tools import (
    get_dau,
    get_learning,
    get_quality
)


# =========================
# 1. 分析 DAU 异常
# =========================

def analyze_dau_anomaly():

    print("\n========== 异常原因分析 ==========")

    # =========================
    # 查询 DAU
    # =========================

    print("\n[Analysis] 查询 DAU...")

    dau_result = get_dau()

    print("[Analysis] DAU 数据：")
    print(dau_result)

    if not dau_result.get("data"):

        return {
            "status": "insufficient_data",
            "conclusion": "暂无足够的 DAU 数据进行分析。",
            "evidence": [],
            "suggestion": "检查 ADS 每日指标数据是否正常生成。"
        }

    data = dau_result["data"]

    if len(data) < 2:

        return {
            "status": "insufficient_data",
            "conclusion": "DAU 数据不足两天，无法进行对比分析。",
            "evidence": data,
            "suggestion": "至少需要两天的 DAU 数据。"
        }

    # =========================
    # 今天 / 昨天
    # =========================

    today = data[0]
    yesterday = data[1]

    today_dau = today["active_user_count"]
    yesterday_dau = yesterday["active_user_count"]

    change = dau_result["change"]
    change_rate = dau_result["change_rate"]

    # =========================
    # 判断 DAU 是否下降
    # =========================

    if change >= 0:

        return {
            "status": "normal",
            "conclusion": "今天 DAU 没有下降。",
            "evidence": {
                "today": today,
                "yesterday": yesterday,
                "change": change,
                "change_rate": change_rate
            },
            "suggestion": "当前无需针对 DAU 下降进行处理。"
        }

    print("\n[Analysis] 检测到 DAU 下降。")

    # =========================
    # 查询用户行为
    # =========================

    print("\n[Analysis] 查询用户行为趋势...")

    behavior_result = get_learning()

    print("[Analysis] 用户行为数据：")
    print(behavior_result)

    # =========================
    # 整理今天 / 昨天行为数据
    # =========================

    behavior_data = {}

    for item in behavior_result:

        date = str(item["stat_date"])
        behavior_type = item["behavior_type"]
        count = item["behavior_count"]

        if date not in behavior_data:

            behavior_data[date] = {}

        behavior_data[date][behavior_type] = count

    dates = sorted(behavior_data.keys(), reverse=True)

    if len(dates) < 2:

        return {
            "status": "insufficient_data",
            "conclusion": (
                f"DAU 从 {yesterday_dau} 下降到 {today_dau}，"
                "但用户行为数据不足，暂时无法进一步判断原因。"
            ),
            "evidence": {
                "dau": {
                    "today": today_dau,
                    "yesterday": yesterday_dau,
                    "change": change,
                    "change_rate": change_rate
                }
            },
            "suggestion": "建议检查用户行为明细数据。"
        }

    today_date = dates[0]
    yesterday_date = dates[1]

    today_behavior = behavior_data[today_date]
    yesterday_behavior = behavior_data[yesterday_date]

    # =========================
    # 计算每种行为变化率
    # =========================

    behavior_changes = []

    all_behavior_types = set(
        today_behavior.keys()
    ) | set(
        yesterday_behavior.keys()
    )

    for behavior_type in all_behavior_types:

        today_count = today_behavior.get(
            behavior_type,
            0
        )

        yesterday_count = yesterday_behavior.get(
            behavior_type,
            0
        )

        change = today_count - yesterday_count

        if yesterday_count != 0:

            change_rate = round(
                change / yesterday_count * 100,
                2
            )

        else:

            change_rate = 0

        behavior_changes.append(
            {
                "behavior_type": behavior_type,
                "today": today_count,
                "yesterday": yesterday_count,
                "change": change,
                "change_rate": change_rate
            }
        )

    # =========================
    # 按下降幅度排序
    # =========================

    behavior_changes.sort(
        key=lambda x: x["change_rate"]
    )

    # =========================
    # 查询数据质量
    # =========================

    print("\n[Analysis] 查询数据质量...")

    quality_result = get_quality()

    print("[Analysis] 数据质量：")
    print(quality_result)

    quality_errors = []

    for item in quality_result:

        if item["status"] != "PASS":

            quality_errors.append(item)

    # =========================
    # 判断原因
    # =========================

    if quality_errors:

        conclusion = (
            f"今天 DAU 从 {yesterday_dau} "
            f"下降到 {today_dau}，"
            f"下降 {abs(change_rate)}%。"
            "同时数据质量检查存在异常，"
            "当前应优先排查数据链路。"
        )

        suggestion = (
            "优先检查用户行为数据采集、ETL、"
            "DWD/DWS/ADS 数据处理链路。"
        )

    else:

        # 找下降最明显的行为
        declining_behaviors = [
            item
            for item in behavior_changes
            if item["change"] < 0
        ]

        if declining_behaviors:

            main_behavior = declining_behaviors[0]

            conclusion = (
                f"今天 DAU 从 {yesterday_dau} "
                f"下降到 {today_dau}，"
                f"下降 {abs(change_rate)}%。"
                f"其中 {main_behavior['behavior_type']} "
                f"行为下降最明显，"
                f"从 {main_behavior['yesterday']} "
                f"下降到 {main_behavior['today']}，"
                f"变化 {main_behavior['change_rate']}%。"
                "当前更倾向于用户活跃行为下降，"
                "而不是数据质量异常。"
            )

            suggestion = (
                "建议进一步检查该行为对应的业务页面、"
                "用户访问情况以及数据采集链路。"
            )

        else:

            conclusion = (
                f"今天 DAU 从 {yesterday_dau} "
                f"下降到 {today_dau}，"
                "但用户行为没有明显下降，"
                "当前无法确定具体业务原因。"
            )

            suggestion = (
                "建议进一步增加渠道、课程、地区等维度进行分析。"
            )

    # =========================
    # 返回最终分析结果
    # =========================

    return {

        "status": "anomaly",

        "conclusion": conclusion,

        "evidence": {

            "dau": {
                "today": today,
                "yesterday": yesterday,
                "change": change,
                "change_rate": change_rate
            },

            "behavior_changes": behavior_changes,

            "quality": quality_result

        },

        "suggestion": suggestion
    }

# =========================
# 2. 测试
# =========================

if __name__ == "__main__":

    result = analyze_dau_anomaly()

    print("\n========== 分析结果 ==========")

    print(result)