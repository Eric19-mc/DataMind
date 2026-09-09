from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment


def main():

    # 创建 Flink 执行环境
    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    # 创建测试数据
    data = [
        ("U000001", "view"),
        ("U000002", "favorite"),
        ("U000003", "start_learning"),
        ("U000004", "finish"),
    ]

    stream = env.from_collection(
        data,
        type_info=Types.TUPLE([
            Types.STRING(),
            Types.STRING()
        ])
    )

    # 打印数据
    stream.print()

    # 执行
    env.execute("DataMind First Flink")


if __name__ == "__main__":
    main()