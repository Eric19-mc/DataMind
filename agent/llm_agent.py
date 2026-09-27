import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from prompts import SYSTEM_PROMPT

from tools import (
    tools,
    get_dau,
    get_course_hot,
    get_learning,
    get_quality
)

from anomaly import analyze_dau_anomaly

# =========================
# 1. 加载环境变量
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)


# =========================
# 2. Agent
# =========================

def ask_agent(question):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": question
        }

    ]

    # =========================
    # Agent 多轮 Tool Calling
    # =========================

    while True:

        response = client.chat.completions.create(
            model="deepseek-v4-flash-ga-260731",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # =========================
        # 没有 Tool
        # =========================

        if not message.tool_calls:

            return message.content

        # =========================
        # 保存 Agent 消息
        # =========================

        messages.append(message)

        # =========================
        # 执行所有 Tool
        # =========================

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            if tool_name == "get_dau":

                print("\n[Agent] 调用工具：get_dau")

                result = get_dau()

            elif tool_name == "get_course_hot":

                print("\n[Agent] 调用工具：get_course_hot")

                result = get_course_hot()

            elif tool_name == "get_learning":

                print("\n[Agent] 调用工具：get_learning")

                result = get_learning()

            elif tool_name == "get_quality":

                print("\n[Agent] 调用工具：get_quality")

                result = get_quality()

            elif tool_name == "analyze_dau_anomaly":

                print("\n[Agent] 调用工具：analyze_dau_anomaly")

                result = analyze_dau_anomaly()

            else:

                print(
                    f"\n[Agent] 未知工具：{tool_name}"
                )

                result = {
                    "error": f"未知工具：{tool_name}"
                }

            # =========================
            # 打印数据库结果
            # =========================

            print("[Agent] 数据库返回：")
            print(result)

            # =========================
            # 把 Tool 结果返回给 Agent
            # =========================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str
                    )
                }
            )


# =========================
# 3. 主程序
# =========================

def main():

    print("=" * 60)
    print("       DataMind LLM Agent")
    print("       DeepSeek-V4-Flash")
    print("       Tools: DAU + Course Hot + Learning + Quality")
    print("       输入 ('exit','quit','退出') 退出")
    print("=" * 60)

    while True:

        question = input("\n请输入问题：").strip()

        if not question:

            continue

        if question.lower() in ["exit", "quit","退出"]:

            print("Agent 已退出。")

            break

        try:

            answer = ask_agent(question)

            print("\n========== Agent ==========")
            print(answer)
            print("============================")

        except Exception as e:

            print("\nAgent 运行失败：")
            print(e)


if __name__ == "__main__":

    main()