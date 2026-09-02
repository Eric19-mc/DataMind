**DataMind：AI 驱动的数据开发与治理平台**

![Image](https://images.openai.com/static-rsc-4/D4clvzEcf932iZejA0uIS_8IupOYmX6z9xPgHCH5fkgQdFDJaI-0q4LUoGnfAPSpVe-HdYyzN7BDC2ZT1WFz7kWktUU9xRwS3J6RRfTvnLO2Ld7nv9ZHkZJyOeUUQp6JEYO4KrnrcHvCkhHejHFYYYZHyvwP3yMWeEnYCi3jpOcBwKccTF2E9bVpa9IuqdIc?purpose=fullsize)
面向在线学习场景的数据开发治理平台，基于MySQL、Hive、Spark、Kafka、Flink、Redis搭建离线+实时数据链路，集成数据质量、血缘、指标管理、AI Agent，实现数据采集‑加工‑治理‑智能分析全流程。

普通项目：数据库→写SQL→输出报表
DataMind流程：业务数据→采集存储→离线/实时计算→数据治理（质量、血缘、指标）→AI Agent→智能数据分析
核心是串联大数据完整开发链路，而非单一技术demo。

## 业务模拟：在线教育平台
业务流程：用户注册→浏览/收藏课程→学习观看→产生学习记录→购买课程
核心数据表：
1. user 用户：id、用户名、年龄、性别、省份、注册时间
2. course 课程：id、课程名、分类、讲师、价格、创建时间
3. user_behavior 用户行为：浏览、收藏、学习、完成、购买
4. order 订单：订单id、用户id、课程id、金额、状态、时间
5. learning_record 学习记录：日期、时长、进度

## 项目架构
DataMind
├─离线：MySQL → Hive → Spark
└─实时：Kafka → Flink → Redis
        ↓
    数据治理层（数据质量、数据血缘、指标管理）
        ↓
    AI Agent（SQL/质量/血缘工具）
        ↓
    数据分析

### 技术职责
Python：数据生成、ETL、工具开发
MySQL：业务数据源
Hive：离线数仓
Spark：离线大规模计算
Kafka：实时消息传输
Flink：实时计算
Redis：实时指标缓存
Git：版本管理
数据质量：异常校验
数据血缘：追溯数据流向
AI Agent：智能查询诊断

通俗类比：MySQL业务库，Kafka传送带，Hive大仓库，Spark加工厂，Flink实时加工厂，Redis查询柜台，治理模块是仓库管理员，AI Agent是数据分析师。

## 离线数仓链路（ODS‑DWD‑DWS‑ADS）
1. ODS原始层：同步MySQL原始数据，保留原貌
2. DWD明细层：清洗脏数据、去重、字段标准化
3. DWS汇总层：按日做用户、课程、订单主题聚合统计
4. ADS应用层：输出GMV、日活、购买率、留存率等指标，供BI与AI调用

## 实时链路
用户行为事件→Kafka→Flink实时计算→Redis缓存→可视化大屏
输出实时在线人数、5分钟浏览/购买量、实时GMV，解决离线T+1延迟。

## 差异化亮点：数据治理
1. **数据质量**：校验空值、负数、重复、格式异常；监控指标环比波动，异常告警。例订单量环比暴跌自动识别并告警。
2. **数据血缘**：完整记录数据流转链路，从业务库到ADS指标逆向溯源，快速定位问题源头。

## AI Agent智能分析
用户自然语言提问（如“今日订单为什么下降”），自动识别指标、查口径、生成SQL、查询数据、校验质量、追溯血缘，输出完整分析结论。并非简单大模型+数据库，AI会调用整套数据治理能力做分析。

## 项目能力覆盖
PythonETL、MySQL高级SQL、四层数仓、PySpark、Hive数仓、Kafka/Flink实时开发、数据质量与血缘治理、AI Agent文本转SQL与智能分析。

## 分阶段迭代开发
阶段1：Python造数+MySQL+Python‑ETL，完成ODS/DWD/DWS/ADS
阶段2：迁移ETL至PySpark
阶段3：Hadoop+Hive搭建企业数仓
阶段4：Kafka+Flink实时链路
阶段5：实现数据质量、血缘模块
阶段6：接入AI Agent
