from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment


def main():
    # 1. 创建 Flink 执行环境
    env = StreamExecutionEnvironment.get_execution_environment()

    # 2. 设置并行度
    env.set_parallelism(1)

    # 3. 模拟用户行为数据
    data = [
        ("U000001", "view"),
        ("U000002", "favorite"),
        ("U000003", "start_learning"),
        ("U000004", "finish"),
    ]

    # 4. 创建数据流
    stream = env.from_collection(
        data,
        type_info=Types.TUPLE([
            Types.STRING(),
            Types.STRING()
        ])
    )

    # 5. 打印数据
    stream.print()

    # 6. 执行 Flink 作业
    env.execute("DataMind First Flink")


if __name__ == "__main__":
    main()