Hive 常用 SQL 备忘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-04-04%2021%3A12%3A06&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: Hive*

<!--START_SECTION:toc-->
- [构造临时数据](#构造临时数据)
- [集合操作](#集合操作)
    - [collect + sort + truncate](#collect--sort--truncate)
- [References](#references)
<!--END_SECTION:toc-->


## 构造临时数据

```sql
-- 法1
SELECT inline(array(
          struct('A', 10, date '2015-01-01')
        , struct('B', 20, date '2016-02-02')
    )) AS (col1, col2, col3);

-- 法2 (推荐)
SELECT stack(2 -- 表示下面有两条数据
        , 'A', 10, date '2015-01-01'
        , 'B', 20, date '2016-01-01'
    ) AS (col0, col1, col2);
```


## 集合操作

### collect + sort + truncate
```sql
ADD JAR hdfs://path_to_brickhouse.jar;
CREATE TEMPORARY FUNCTION truncate_array AS 'brickhouse.udf.collect.TruncateArrayUDF';

-- truncate_array 截取数组时, 长度不够会补 NULL
SELECT pkey, IF(size(items_sort) > 5, truncate_array(items_sort, 5), items_sort) AS items_sort
FROM (
    SELECT pkey, sort_array(collect_set(struct(-score, item))).col2 AS items_sort
    FROM (
        SELECT pkey, item, score
        FROM ...
    ) A
    GROUP BY pkey
) A
;
```


## References
