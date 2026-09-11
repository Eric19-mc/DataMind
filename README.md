# DataMind

> AI 驱动的数据开发与治理平台

DataMind 是一个面向数据开发与数据治理场景的综合实践项目，构建从数据采集、离线/实时数据处理、数据仓库、数据质量治理到 AI Agent 智能分析的完整数据链路。

## 一、项目架构

```text
                    DataMind Agent
                         │
                         ↓
                 LLM Tool Calling
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
        DAU Tool     行为分析 Tool    质量 Tool
          ↓              ↓              ↓
        MySQL          MySQL          MySQL
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                  异常原因分析引擎
                         ↓
                  原因判断 + 数据证据
                         ↓
                    处理建议
```

## 二、数据处理链路

```text
数据生成
   ↓
CSV
   ↓
MySQL
   ↓
ODS
   ↓
DWD
   ↓
DWS
   ↓
ADS
   ↓
┌───────────────┐
│               │
Spark           Kafka
│               │
↓               ↓
离线计算        实时数据
                ↓
              Flink
                ↓
              Redis
```

## 三、主要技术

* Python
* SQL
* MySQL
* Hadoop
* HDFS
* Spark / PySpark
* Kafka
* Flink / PyFlink
* Redis
* LLM
* Tool Calling

## 四、项目功能

### 1. 数据生成

通过 Python 模拟用户、课程以及用户行为数据，为数据开发和分析提供测试数据。

主要数据包括：

```text
user.csv
course.csv
user_behavior.csv
```

### 2. 数据仓库

基于 ODS → DWD → DWS → ADS 分层思想进行数据处理。

主要包括：

* ODS 原始数据层
* DWD 明细数据层
* DWS 汇总数据层
* ADS 应用数据层

### 3. 离线数据处理

使用 PySpark 对业务数据进行清洗、转换和聚合，生成用户活跃度、课程热度、用户学习等 ADS 指标。

### 4. 实时数据处理

使用 Kafka 模拟用户行为数据流，通过 Flink 进行实时数据处理，并结合 Redis 保存实时计算结果。

### 5. 数据质量

建立数据质量规则，对数据进行质量检查，并将检查结果写入 MySQL。

可以检测：

* 数据完整性
* 数据异常
* 字段质量
* 规则执行结果

### 6. AI Agent

基于 LLM Tool Calling 构建 DataMind Agent。

Agent 可以根据用户问题自主选择数据查询工具。

目前支持：

```text
get_dau
get_course_hot
get_learning
get_quality
analyze_dau_anomaly
```

### 7. 异常原因分析

针对：

> 为什么今天活跃用户下降了？

Agent 可以自动：

```text
查询 DAU
   ↓
判断 DAU 是否下降
   ↓
查询用户行为趋势
   ↓
查询数据质量
   ↓
综合判断异常原因
   ↓
返回数据证据
   ↓
生成处理建议
```

## 五、项目示例

用户输入：

```text
为什么今天活跃用户下降了？
```

Agent 自动调用异常分析工具，对最近两天 DAU、用户行为以及数据质量进行分析。

最终输出：

```text
异常结论
+
DAU 变化幅度
+
用户行为变化
+
数据质量情况
+
处理建议
```

## 六、项目目录

```text
DataMind
│
├── agent
│   ├── llm_agent.py
│   ├── prompts.py
│   ├── tools.py
│   └── anomaly.py
│
├── data-generator
│   ├── generator.py
│   └── data
│
├── mysql
│   ├── init.sql
│   ├── etl_pipeline.py
│   └── load_ads.py
│
├── spark
│   └── ...
│
├── kafka
│   ├── producer.py
│   └── consumer.py
│
├── flink
│   └── ...
│
├── redis
│   └── ...
│
├── data-quality
│   └── ...
│
├── lineage
│   └── ...
│
└── README.md
```

## 七、项目特点

DataMind 不只是单独使用某一个大数据组件，而是将：

```text
数据开发
+
数据仓库
+
离线计算
+
实时计算
+
数据治理
+
AI Agent
```

结合到一个完整项目中。

其中 AI Agent 通过 Tool Calling 访问真实数据库，并根据业务问题选择不同的数据分析工具，实现从：

```text
用户问题
    ↓
数据查询
    ↓
指标分析
    ↓
异常判断
    ↓
数据证据
    ↓
业务建议
```

的完整闭环。

## 八、项目定位

本项目主要用于学习和实践：

* 数据开发
* 数据仓库
* 大数据离线计算
* 大数据实时计算
* 数据质量治理
* AI Agent 数据应用

同时作为数据开发岗位的项目实践案例。
