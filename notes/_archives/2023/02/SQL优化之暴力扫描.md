SQL优化之暴力扫描
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: sql优化, hive sql, hql*

<!--START_SECTION:toc-->
- [背景](#背景)
- [解决方案](#解决方案)
    - [法1) 提取中间表](#法1-提取中间表)
    - [法2) 滑动窗口](#法2-滑动窗口)
        - [例1: 滑动计算统计数据](#例1-滑动计算统计数据)
        - [例2: 保存所有数据](#例2-保存所有数据)
        - [例3: 通过最新日期过滤](#例3-通过最新日期过滤)
<!--END_SECTION:toc-->

## 背景
- 例行任务每天暴力扫描上游任务的多个分区，造成了资源浪费。
- 示例:
    ```sql
    SELECT A.query, COUNT(1) AS n_clk
    FROM dbtable A
    WHERE A.dt > DATA_SUB('$today', 60)
    GROUP BY A.query
    ```
    - 该任务每天扫描历史60天的数据, 统计 query 的点击数, 但其实每天有 59 天是重复扫描的;

## 解决方案

### 法1) 提取中间表
- 一般出现暴力扫描主要原因是总数据量太大; 一般是因为上游表是一张宽表, 保存了太多数据;
- 中间表就是把需要的数据单独取出来, 也按天存储; 然后下游扫描这张小表即可;
- 这个方法非常简单, 缺点是需要回跑天数较多, 有些平台可能会有限制;

### 法2) 滑动窗口

- 注意滑动窗口并不一定能降低资源, 如果源表不大的话, 反而会增加消耗的资源;

#### 例1: 滑动计算统计数据
```sql
-- 先执行前一天的汇总数据
INSERT OVERWRITE TABLE target_table PARTITION( dt = '$yesterday' )
SELECT A.query, COUNT(1) AS n_clk
FROM src_table A
WHERE A.dt > DATA_SUB('$yesterday', 60)
GROUP BY A.query
;

-- 更新
SELECT
FROM (
    -- 前一天的汇总数据
    SELECT A.query, A.n_clk
    FROM target_table A
    WHERE A.dt = '$yesterday'

    UNION ALL

    -- 加上今天的数据
    SELECT A.query, COUNT(1) AS n_clk
    FROM src_table A
    WHERE A.dt = '$today'
    GROUP BY A.query

    UNION ALL

    -- 减去60天前的数据
    SELECT A.query, -1*COUNT(1) AS n_clk
    FROM src_table A
    WHERE A.dt = DATA_SUB('$today', 60)
    GROUP BY A.query

    -- 或者可以把上面的两天合并在一起写
    -- SELECT A.query
    --     ,  if(A.dt = '$today', COUNT(1), -1*COUNT(1)) AS n_clk
    -- FROM src_table A
    -- WHERE A.dt in ('$today', DATA_SUB('$today', 60))
    -- GROUP BY A.query
) A
```
- 这里要注意一点, 如果上游表 `src_table` 只保存 60 天的数据, 那么要小心 `DATA_SUB('$today', 60)` 的操作, 因为这实际上是前 61 天的数据, 可能不存在, 此时 `n_clk` 会一直增加;


#### 例2: 保存所有数据
- 如果是无法滑动计算的特征, 那么可以考虑把历史数据都保存下来;
- 仅适用于**聚合表**;

```sql
-- 先执行前一天的汇总数据
INSERT OVERWRITE TABLE target_table PARTITION( dt = '$yesterday' )
SELECT A.query
    ,  str_to_map(concat_ws(',', collect_list(concat_ws(':', A.dt, CAST(A.n_clk AS string))))) AS data_map
    -- str_to_map 默认使用 ',' 和 ':' 分割
FROM (
    SELECT A.query, A.dt, COUNT(1) AS n_clk
    FROM src_table A
    WHERE A.dt > DATA_SUB('$yesterday', 60)
    GROUP BY A.query, A.dt
) A
GROUP BY A.query
;

-- 更新
SELECT A.query
    ,  str_to_map(concat_ws(',', collect_list(concat_ws(':', A.dt, CAST(A.n_clk AS string))))) AS data_map
FROM (
    SELECT A.query, B.dt, B.n_clk
    FROM target_table A
        LATERAL VIEW explode(A.data) B AS dt, n_clk
    WHERE A.dt = '$yesterday'
      AND B.dt > DATA_SUB('$today', 60)

    UNION ALL

    -- 加上今天的数据
    SELECT A.query, A.dt, COUNT(1) AS n_clk
    FROM src_table A
    WHERE A.dt = '$today'
    GROUP BY A.query, A.dt
) A
```

#### 例3: 通过最新日期过滤

```sql
-- 先执行前一天的汇总数据
INSERT OVERWRITE TABLE target_table PARTITION( dt = '$yesterday' )
SELECT A.query
    ,  max(A.dt) AS latest_dt
FROM src_table A
WHERE A.dt > DATA_SUB('$yesterday', 30)
GROUP BY A.query
;

-- 更新
SELECT A.query, A.latest_dt
FROM (
    SELECT COALESCE(B.query, A.query) AS query
        ,  COALESCE(B.dt, 
                    if(A.latest_dt > DATA_SUB('$today', 30), 
                       A.latest_dt, '-1')) AS latest_dt
    FROM (
        SELECT A.query, A.latest_dt
        FROM target_table A
        WHERE A.dt = '$yesterday'
    ) A
    FULL JOIN (
        SELECT A.query, A.dt
        FROM src_table A
        WHERE A.dt = '$today'
    ) B
    ON A.query = B.query
) A
WHERE A.latest_dt != '-1'
;
```
