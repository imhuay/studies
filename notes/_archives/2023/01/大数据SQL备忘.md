Hive/Spark/Presto SQL 备忘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-02-19%2020%3A11%3A02&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: Hive SQL, Spark SQL, Presto SQL*

<!--START_SECTION:toc-->
- [参考资料](#参考资料)
    - [复杂案例](#复杂案例)
- [数据类型](#数据类型)
    - [基本类型 TODO](#基本类型-todo)
    - [容器类型](#容器类型)
- [常用 DDL](#常用-ddl)
    - [建表 (`CREATE`)](#建表-create)
        - [临时表](#临时表)
    - [修改 (`ALTER`)](#修改-alter)
        - [修改列](#修改列)
        - [增加列](#增加列)
- [常用查询/技巧](#常用查询技巧)
    - [聚合操作 (`GROUP BY`)](#聚合操作-group-by)
        - [排序 `sort_array(collect_list(...))`](#排序-sort_arraycollect_list)
    - [侧视图 (`LATERAL VIEW`)](#侧视图-lateral-view)
        - [侧视图 for Presto (`CROSS JOIN`)](#侧视图-for-presto-cross-join)
    - [子查询 (`WITH t AS (...)`)](#子查询-with-t-as-)
    - [数组操作](#数组操作)
    - [分页](#分页)
    - [构造示例/测试数据](#构造示例测试数据)
    - [对称去重 (基于 `sort_array`)](#对称去重-基于-sort_array)
- [常用函数/UDF](#常用函数udf)
    - [字符串](#字符串)
    - [数学](#数学)
    - [聚合函数](#聚合函数)
    - [条件函数](#条件函数)
        - [`CASE WHEN`](#case-when)
    - [表生成函数 (UDTF)](#表生成函数-udtf)
    - [Python Transform 用法](#python-transform-用法)
        - [Map-Reduce 语法](#map-reduce-语法)
    - [窗口与分析函数](#窗口与分析函数)
        - [排序 (`ROW_NUMBER/RANK/DENSE_RANK`)](#排序-row_numberrankdense_rank)
        - [切片 (`NTILE`) TODO](#切片-ntile-todo)
        - [去重 (基于 `ROW_NUMBER`)](#去重-基于-row_number)
- [配置属性](#配置属性)
    - [Hive](#hive)
- [其他](#其他)
    - [`DISTINCT` 和 `GROUP BY` 在去重时有区别吗?](#distinct-和-group-by-在去重时有区别吗)
    - [web 模板变量](#web-模板变量)
    - [从 Hive 迁移到 Presto](#从-hive-迁移到-presto)
- [异常记录](#异常记录)
    - [对 `f(col)` 分组或排序](#对-fcol-分组或排序)
    - [日期加减](#日期加减)
    - [`AS` 多个别名时要不要括号?](#as-多个别名时要不要括号)
    - [自动类型转换](#自动类型转换)
    - [规避暴力扫描警告](#规避暴力扫描警告)
<!--END_SECTION:toc-->


## 参考资料
- [Hive SQL - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual)
    - [Hive SQL build-in Functions - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF)
- [Spark SQL and DataFrames - Spark Documentation](https://spark.apache.org/docs/latest/sql-programming-guide.html)
    - [Functions - Spark Documentation](https://spark.apache.org/docs/latest/sql-ref-functions.html)
    - [Spark SQL, Built-in Functions](https://spark.apache.org/docs/latest/api/sql)
- [Presto Documentation](https://prestodb.io/docs/current/)
    - [Migrating From Hive — Presto Documentation](https://prestodb.io/docs/current/migration/from-hive.html)
    - [Presto学习之路 -- 01.整体介绍 - 知乎](https://zhuanlan.zhihu.com/p/111053544)

### 复杂案例
- [信息熵/信息增益计算](./sql-计算信息熵与信息增益.md)


## 数据类型

### 基本类型 TODO

### 容器类型
- 主要有 4 中容器类型: 
    - `ARRAY<data_type>`
    - `MAP<primitive_type, data_type>`
    - `STRUCT<col_name : data_type [COMMENT col_comment], ...>`
    - `UNIONTYPE<data_type, data_type, ...>` (一般不使用)

**基本构造函数**
> [Complex Type Constructors - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF#LanguageManualUDF-ComplexTypeConstructors)
```sql
-- ARRAY
SELECT array(1,2,3);  -- [1,2,3]
SELECT array('a','b','c')[0];  -- "a"

-- MAP
SELECT map('a', 1), map('b', '2', 'c', 3);
-- {"a":1}  {"b":"2","c":"3"}  -- 注意, 整数 3 转成了字符串 3
SELECT map('a', 1)['a'];  -- 1

-- struct
SELECT struct('a', 1, ARRAY(1,2,3));  -- {"col1":"a","col2":1,"col3":[1,2,3]}
SELECT struct('a', 1, ARRAY(1,2,3)).col2;  -- 1
-- named_struct
SELECT named_struct('c1', 'a', 'c2', 1, 'c3', ARRAY(1,2,3));  -- {"c1":"a","c2":1,"c3":[1,2,3]}
SELECT named_struct('c1', 'a', 'c2', 1, 'c3', ARRAY(1,2,3)).c2;  -- 1

-- ARRAY + struct
SELECT array(struct('a', 1), struct('b', 2), struct('c', 3)).col1;  -- ["a","b","c"]
-- ARRAY + named_struct
SELECT array(named_struct('c1', 'a', 'c2', 1), named_struct('c1', 'b', 'c2', 2), named_struct('c1', 'c', 'c2', 3)).c1;  -- ["a","b","c"]
```

## 常用 DDL
> 数据定义语言 (Data Definition Language, DDL)

### 建表 (`CREATE`)
> [CreateTable - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-CreateTable)
```sql
-- 示例 1: 分区表, 
CREATE TABLE db_name.table_name (
    `column_1`      string COMMENT '列注释1'
    , `column_2`    bigint COMMENT '列注释2'
    , `column_3`    double COMMENT '列注释3'
    , `column_4`    array < string > COMMENT '列注释4'
) COMMENT 'datastudio 表ddl模板' 
PARTITIONED BY (
  `pt` string COMMENT '分区注释1' 
  [, `hr` string COMMENT '分区注释2']
)
STORED AS ORC   -- 一种压缩格式
;

-- 示例 2: 外部 text 数据
CREATE EXTERNAL TABLE page_view (
    viewTime INT, userid BIGINT,
    page_url STRING, referrer_url STRING,
    ip STRING COMMENT 'IP Address of the User',
    country STRING COMMENT 'country of origination'
)
COMMENT 'This is the staging page view table'
ROW FORMAT DELIMITED    -- 指定行分隔符, 配合文本格式使用
    FIELDS TERMINATED BY '\t'   -- 列分割
    LINES TERMINATED BY '\n'    -- 行分割 (默认)
STORED AS TEXTFILE      -- 存储为文本格式
LOCATION '<hdfs_location>'
;

-- 示例 3: Create Table As Select
CREATE TABLE new_key_value_store
   ROW FORMAT SERDE "org.apache.hadoop.hive.serde2.columnar.ColumnarSerDe"
   STORED AS RCFile     -- 一种文件格式
   AS   -- 不指定列时, 直接使用查询结果的列名和类型 (无注释)
SELECT 
    (key % 1024) AS new_key
    , concat(key, value) AS key_value_pair
FROM key_value_store
SORT BY new_key, key_value_pair  -- 
;
```

#### 临时表
- 注意: Hive 和 Spark 中的临时表语法不同; 
```sql
-- Hive
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_table AS
SELECT ...
;

-- Spark
CACHE TABLE tmp_table AS
SELECT ...
;

-- Hive/Spark 都适用 (如果公司支持自动删除临时表, 推荐这种写法)
-- 物理临时表, 一些脚本中使用, 易于调试, 可重复使用;
DROP TABLE IF EXISTS db.tmp_task_tabel;
CREATE TABLE db.tmp_tabel AS
SELECT  ...
```
> ***物理临时表使用注意事项 :*** 
> *1) 使用物理临时表时, 一定要添加任务相关的标识, 如 `db.tmp_taskname_tablename`, 否则可能导致在不用任务间依赖相同的临时表, 当临时表在其中一个任务中被删除时, 另一个任务执行失败; 2) 系统支持自动删除 `tmp` 表, 或者在脚本末尾手动删除;*

### 修改 (`ALTER`)
> [Alter Table/Partition/Column - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-AlterTable/Partition/Column)

#### 修改列
> [Change Column Name/Type/Position/Comment - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-ChangeColumnName/Type/Position/Comment)

- 一条 `ALTER` 语句一次只能修改一列;
```sql
-- 语法
ALTER TABLE table_name [PARTITION partition_spec] CHANGE [COLUMN] col_old_name col_new_name column_type
  [COMMENT col_comment] [FIRST|AFTER column_name] [CASCADE|RESTRICT];

-- 基础示例
ALTER TABLE db.table CHANGE a x BIGINT COMMENT 'column x';  -- 修改列名
ALTER TABLE db.table CHANGE b b STRING COMMENT 'column b';  -- 修改类型 (名字不变)
```

#### 增加列
> [Add/Replace Columns - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-Add/ReplaceColumns)

- 一条 `ALTER` 语句一次只能修改一列, 但是能增加多列;
```sql
-- 语法
ALTER TABLE table_name 
  [PARTITION partition_spec]                 -- (Note: Hive 0.14.0 and later)
  ADD|REPLACE COLUMNS (col_name data_type [COMMENT col_comment], ...)
  [CASCADE|RESTRICT]                         -- (Note: Hive 1.1.0 and later)

-- 基础示例
ALTER TABLE db.table
ADD COLUMNS (
    a BIGINT    COMMENT 'column a'
    , b STRING  COMMENT 'column b'
)
```


## 常用查询/技巧
> 数据查询语言 (Data Query Language, DQL)

### 聚合操作 (`GROUP BY`)

#### 排序 `sort_array(collect_list(...))`
> [hiveql - Sorting within collect_list() in hive - Stack Overflow](https://stackoverflow.com/questions/50766764/sorting-within-collect-list-in-hive/72458308#72458308)

```sql
SELECT key
    , sort_array(collect_list(STRUCT(-cnt, item_cnt_pair))).col2 as item_cnt_list_sorted
    -- col2 为 STRUCT 中的默认列名, 负号表示倒序排列
FROM
(
    SELECT key, cnt
        , concat(item, ':', cnt) AS item_cnt_pair  -- 可以通过 SPLIT 取值
        -- , STRUCT(item, cnt) AS item_cnt_pair  -- 根据 STRUCT 的默认列名取值
        -- , MAP(item, cnt) AS item_cnt_pair  -- 可以利用 map_keys/map_values 取值
    FROM
    (
        SELECT key, item, count(1) AS cnt
        -- FROM db.some_table A
        FROM (
            SELECT 'A' AS key, 'red' AS item UNION ALL
            SELECT 'A' AS key, 'red' AS item UNION ALL
            SELECT 'A' AS key, 'blue' AS item UNION ALL
            SELECT 'A' AS key, 'blue' AS item UNION ALL
            SELECT 'A' AS key, 'yellow' AS item UNION ALL
            SELECT 'A' AS key, 'yellow' AS item UNION ALL
            SELECT 'A' AS key, 'yellow' AS item UNION ALL
            SELECT 'B' AS key, 'yellow' AS item UNION ALL
            SELECT 'B' AS key, 'yellow' AS item UNION ALL
            SELECT 'B' AS key, 'green' AS item
        ) A
        GROUP BY key, item
    ) A
) A
GROUP BY key
;
-- A, ["yellow:3","blue:2","red:2"]
-- B, ["yellow:2","green:1"]
```
- `sort_array(collect_list(STRUCT(cnt, item_cnt_pair))).col2` 相当于 python 中的对一个**元组列表**进行排序, 排序的 key 依次从元组中取;
    - 一般情况下, 先排序(`ORDER/SORT BY`), 再 `collect_list` 也可以, 但是速度比较慢;


### 侧视图 (`LATERAL VIEW`)
```sql
-- 语法
lateralView: LATERAL VIEW udtf(expression) tableAlias AS columnAlias (',' columnAlias)*
fromClause: FROM baseTable (lateralView)*

-- 示例 1: 基本用法
SELECT A.a, B.b
FROM (SELECT 'id' AS a, array(1,2,3) AS arr) A 
LATERAL VIEW explode(A.arr) B AS b;
-- 产生 3 条数据

-- 示例 2: 多个侧视图, 相当于做了笛卡尔积
SELECT A.a, B.b, C.c
FROM (SELECT 'id' AS a, array(1,2,3) AS arr1, array('a','b','c') AS arr2) A 
LATERAL VIEW explode(A.arr1) B AS b
LATERAL VIEW explode(A.arr2) C AS c;
-- 产生 9 条数据

-- 示例 3: 多个数组并列, 相当于 Python 中的 zip
SELECT A.a, B.b, A.arr2[i] AS c
FROM (SELECT 'id' AS a, array(1,2,3) AS arr1, array('a','b','c') AS arr2) A 
LATERAL VIEW posexplode(A.arr1) B AS i, b;
-- 产生 3 条数据

-- LATERAL VIEW OUTER
SELECT A.a, B.b FROM (SELECT explode(array(1,2,3)) a) A
    LATERAL VIEW explode(array()) B AS b;  -- 结果为空, 相当于 JOIN 中右表为空, 导致整体为空
SELECT A.a, B.b FROM (SELECT explode(array(1,2,3)) a) A
    LATERAL VIEW OUTER explode(array()) B AS b;  -- 结果不为空, 相当于 LEFT JOIN, 不影响左表的结果
```

#### 侧视图 for Presto (`CROSS JOIN`)
> 

Presto 中与 Hive 三个示例对应的写法
> 以下 SQL 未经过测试, 其中构造的 array 的方法在 Presto 中可能有问题;
```sql
-- 示例 1
SELECT A.a, B.b
FROM (SELECT 'id' AS a, array(1,2,3) AS arr) A 
CROSS JOIN UNNEST(A.arr) AS B(b);
-- LATERAL VIEW explode(A.arr) B AS b;
-- 产生 3 条数据

-- 示例 2
SELECT A.a, B.b, C.c
FROM (SELECT 'id' AS a, array(1,2,3) AS arr1, array('a','b','c') AS arr2) A 
CROSS JOIN UNNEST(A.arr1) AS B(b)
-- LATERAL VIEW explode(A.arr1) B AS b
CROSS JOIN UNNEST(A.arr2) AS C(c);
-- LATERAL VIEW explode(A.arr2) C AS c;
-- 产生 9 条数据

-- 示例 3
SELECT A.a, B.b, B.c
-- SELECT A.a, B.b, A.arr2[i] AS c
FROM (SELECT 'id' AS a, array(1,2,3) AS arr1, array('a','b','c') AS arr2) A 
CROSS JOIN UNNEST(A.arr1, A.arr2) AS B(b, c)
-- LATERAL VIEW posexplode(A.arr1) B AS i, b;
-- 产生 3 条数据
```

### 子查询 (`WITH t AS (...)`)
> [Common Table Expression (CTE) - Spark Documentation](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-cte.html)
>> Hive 官方文档没查到相关的语法, 有些环境确实也不支持这个语法;
```sql
-- CTE with multiple column aliases
WITH t(x, y) AS (SELECT 1, 2)
SELECT * FROM t WHERE x = 1 AND y = 2;

-- CTE in subquery
SELECT max(c) FROM (
    WITH t(c) AS (SELECT 1)
    SELECT * FROM t
);

-- 多表
WITH t1 AS (
    SELECT ...
),
t2 AS (
    SELECT ...
),
t3 AS (
    SELECT * FROM t1  -- 可以使用前面子查询的结果
    WHERE ...
)
SELECT * FROM t2 JOIN t3 ON ...;

-- 嵌套 (好像有的 sql 不支持)
WITH t AS (
    WITH t2 AS (SELECT 1)
    SELECT * FROM t2
)
SELECT * FROM t;

-- 嵌套冲突时
SET spark.sql.legacy.ctePrecedencePolicy = CORRECTED;
-- 如果不开启该设置, 会抛 AnalysisException
WITH
    t AS (SELECT 1),
    t2 AS (
        WITH t AS (SELECT 2)
        SELECT * FROM t
    )
SELECT * FROM t2;
```

### 数组操作
- Hive 提供的内置函数较少, 一般使用外部 UDF; Spark 则提供了丰富的数组操作函数, 一般命名为 `array_*`;
- 常用的 Hive UDF 库
    - [brickhouse - Hive](https://github.com/klout/brickhouse);

```sql
-- 以下 函数名 默认兼容 Hive 和 Spark
-- brickhouse
ADD JAR hdfs://path/to/brickhouse.jar;
-- 交集(去重)
CREATE TEMPORARY FUNCTION array_intersect AS "brickhouse.udf.collect.ArrayIntersectUDF";
-- 并集(去重)
CREATE TEMPORARY FUNCTION array_union AS "brickhouse.udf.collect.ArrayUnionUDF";
-- 差集(存在的都移除, 不存在的都保留)
CREATE TEMPORARY FUNCTION array_except AS "brickhouse.udf.collect.SetDifferenceUDF";

-- 以下为 Hive 中测试结果, Spark 未测试
-- 交集
SELECT array_intersect(array(1,2,3,3), array(3,3,4,5));  -- [3]
SELECT array_intersect(array(1,2,2,3,3), array(2,3,3,4,5));  -- [2,3]
SELECT array_intersect(array(1,2,2,3,NULL), array(2,3,3,4,5));  -- [2,3]
SELECT array_intersect(array(1,2,2,3,NULL), array(2,3,3,4,NULL));  -- [null,2,3]
-- 并集
SELECT array_union(array(1,2,3,3), array(3,3,4,5));  -- [1,2,3,4,5]
SELECT array_union(array(1,2,3,NULL), array(3,3,4,5));  -- [null,1,2,3,4,5]
-- 差集
SELECT array_except(array(1,2,2,3), array(1,3,5)); -- [2,2], 不存在的都保留
SELECT array_except(array(1,2,2,3,3), array(1,3,5)); -- [2,2], 存在的都移除
SELECT array_except(array(1,2,2), array(1,2,3)); -- []
-- 判断 a 是否 b 的子集
SELECT size(array_except(array(1,2), array(1,2,3))) = 0;  -- true
SELECT size(array_except(array(1,2,2), array(1,2,3))) = 0;  -- true
SELECT size(array_except(array(1,2,2,NULL), array(1,2,3))) = 0;  -- false
SELECT size(array_except(array(1,2,2), array(1,2,3,NULL))) = 0;  -- true


```

<!-- 
#### 判断子集
- 一个通用的方法是编写 UDF
- 下面是一些 trick 方法

```sql
-- 判断 a 是否 b 的子集
-- 思路是利用 a 构造正则表达式, 判断 b 中是否存在 a 的所有元素
SELECT concat('#',concat_ws('#',b),'#') AS tmp_a
    , concat('#(',concat_ws('|',a),')#') AS tmp_b
    , concat('#',concat_ws('#',b),'#') RLIKE concat('#(',concat_ws('|',a),')#')  AS is_subset
FROM (
    SELECT array('a','b','c') AS a, array('b','c') AS b
    UNION ALL
    SELECT array('a','b','c') AS a, array('b','d') AS b
) A
-- #a#b#c#, #(b|c)#, true
-- #a#b#c#, #(b|d)#, false

```
-->

### 分页
> 使用场景: 限制每次下载/浏览的数据量时

```sql
-- 写法 1: 适用于小数据量, 且不含 ORDER BY 的情况, 如果存在 ORDER BY, 推荐写法 2
SELECT * 
FROM table_name A
WHERE ...
-- ORDER BY ...
LIMIT page_sz OFFSET (page_id - 1) * page_sz
-- LIMIT (page_id - 1) * page_sz, page_sz  -- 等价写法
;

-- 写法 2: 基于 row_number() 给每行添加一个可比较的自增 rn (从 1 开始)
SELECT * FROM (
    SELECT A.*, row_number() over (ORDER BY ...) as rn
    FROM table_name A
    WHERE ...
) A
WHERE rn > (page_id - 1) * page_sz AND rn <= (page_id * page_sz)
-- WHERE rn BETWEEN ((page_id - 1) * page_sz + 1) AND (page_id * page_sz);  -- 等价写法

-- 传统数据库因为存在主键, 还有其他写法, 这里略
```
> [传统数据库 SQL 窗口函数实现高效分页查询的案例分析_MsSql_脚本之家](https://www.jb51.net/article/212864.htm)


### 构造示例/测试数据
> [表生成函数 (UDTF)](#表生成函数-udtf)

### 对称去重 (基于 `sort_array`)
- 对具有对称性的 pair/tuple, 直接使用 `GROUP BY` 无法达到去重的目的, 可以先对 pair/tuple 排序;

```sql
SELECT sort_array(array(A.x, A.y))[0] AS x
    ,  sort_array(array(A.x, A.y))[1] AS y
FROM (
    SELECT inline(array(
        struct('a', 'b'),
        struct('b', 'a'),
        struct('c', 'd'),
        struct('d', 'c'),
    )) AS (x, y)
) A
GROUP BY 1, 2
;
```
> hive 中数组下标从 0 开始; 但一些 sql 是从 1 开始的, 如 presto;

TODO: 当有很多列时, 如何自动展开


## 常用函数/UDF
> [Hive Operators and User-Defined Functions (UDFs) - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF)

### 字符串
```sql
-- 编辑距离: levenshtein(string A, string B) -> int
SELECT levenshtein('kitten', 'sitting');  -- 3

-- context_ngrams

```

### 数学
```sql
-- 最小值: least(T v1, T v2, ...)
SELECT least(3, 1, -1);  -- -1

-- 最大值: greatest(T v1, T v2, ...)
SELECT least(3, 1, -1);  -- 3
```

### 聚合函数
**函数细节**
- `collect_set / collect_list` 不会收集 `NULL` 值

```sql
```

### 条件函数
> [Conditional Functions - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF#LanguageManualUDF-ConditionalFunctions)

#### `CASE WHEN`
```sql
-- 写法 1: When a = b, returns c; when a = d, returns e; else returns f.
CASE a 
    WHEN b THEN c 
    WHEN d THEN e
    -- WHEN ... THEN ...
    ELSE f
END

-- 写法 2: When a is true, returns b; when c is true, returns d; else returns e.
CASE 
    WHEN a THEN b 
    WHEN c THEN d
    -- WHEN ... THEN ...
    ELSE e
END
```

### 表生成函数 (UDTF)
> [Built-in Table-Generating Functions (UDTF) - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF#LanguageManualUDF-Built-inTable-GeneratingFunctions(UDTF))

```sql
-- explode(array)
select explode(array('A','B','C')) as col;


-- explode(map)
select explode(map('A',10,'B',20,'C',30)) as (key,value);
select tf.* from (select 0) t 
    lateral view explode(map('A',10,'B',20,'C',30)) tf as key,value;
-- 注意: AS aliases 这里, 前者要有括号, 后者没有括号!

-- posexplode(array), 不支持 posexplode(map)
select posexplode(array('A','B','C')) as (pos,val);
-- select posexplode(map('A',10,'B',20,'C',30)) as (pos,key,value);  -- 不支持

-- inline(array(struct))
select inline(array(
        struct('A', 10, date '2015-01-01'),
        struct('B', 20, date '2016-02-02'))
    ) as (col1,col2,col3);

-- stack(values)
select stack(2, -- 表示下面有两条数据
    'A', 10, date '2015-01-01',
    'B', 20, date '2016-01-01') as (col0,col1,col2);
```

### Python Transform 用法
> [Transform/Map-Reduce Syntax - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Transform)

#### Map-Reduce 语法
- `MAP ...` 和 `REDUCE ...` 实际上就是 `SELECT TRANSFORM ( ... )` 的语法转换, 即以下两种写法是等价的;
    ```sql
    FROM (
        FROM pv_users A
        MAP A.userid, A.date
        USING 'python map_script.py'
        AS dt, uid
        CLUSTER BY dt
    ) M
    INSERT OVERWRITE TABLE pv_users_reduced
        REDUCE M.dt, M.uid
        USING 'python reduce_script.py'
        AS dt, count
    ;

    -- 等价于
    FROM (
        FROM pv_users A
        SELECT TRANSFORM(A.userid, A.date)
        USING 'python map_script.py'
        AS dt, uid
        CLUSTER BY dt
    ) M
    INSERT OVERWRITE TABLE pv_users_reduced
        SELECT TRANSFORM(M.dt, M.uid)
        USING 'python reduce_script.py'
        AS dt, count
    ;
    ```

**更多示例**
- [Hive-Transform-Python: 快捷的 Map/Reduce - 简书](https://www.jianshu.com/p/8a7b3cf4cac5/)


### 窗口与分析函数
> [Windowing and Analytics Functions - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+WindowingAndAnalytics)
<!-- > [HIVE SQL奇技淫巧 - 知乎](https://zhuanlan.zhihu.com/p/80887746) -->

#### 排序 (`ROW_NUMBER/RANK/DENSE_RANK`)
```sql
SELECT 
    cookieid, pt, pv,
    ROW_NUMBER() OVER(PARTITION BY cookieid ORDER BY pv DESC) AS rn1,   -- 形如 1,2,3,4,5 (最常用)
    RANK() OVER(PARTITION BY cookieid ORDER BY pv DESC) AS rn2,         -- 形如 1,1,3,3,5
    DENSE_RANK() OVER(PARTITION BY cookieid ORDER BY pv DESC) AS rn3    -- 形如 1,1,2,2,3
FROM (
    -- 测试数据
    SELECT cookieid, T.col2[idx] AS pt, T.col3[idx] AS pv
    FROM (
        SELECT ARRAY(
            STRUCT('cookie1', '2015-04-10', 1)
            , STRUCT('cookie1', '2015-04-11', 5)
            , STRUCT('cookie1', '2015-04-12', 7)
            , STRUCT('cookie1', '2015-04-13', 3)
            , STRUCT('cookie1', '2015-04-14', 2)
            , STRUCT('cookie1', '2015-04-15', 4)
            , STRUCT('cookie1', '2015-04-16', 4)
            -- , STRUCT('cookie2', '2015-04-10', 2)
            -- , STRUCT('cookie2', '2015-04-11', 3)
            -- , STRUCT('cookie2', '2015-04-12', 5)
            -- , STRUCT('cookie2', '2015-04-13', 6)
            -- , STRUCT('cookie2', '2015-04-14', 3)
            -- , STRUCT('cookie2', '2015-04-15', 9)
            -- , STRUCT('cookie2', '2015-04-16', 7)
        ) T
    ) A
    LATERAL VIEW posexplode(T.col1) B AS idx, cookieid
) A
;
-- cookieid  pt          pv  rn1 rn2 rn3
-- cookie1   2015-04-12  7   1   1   1
-- cookie1   2015-04-11  5   2   2   2
-- cookie1   2015-04-15  4   3   3   3
-- cookie1   2015-04-16  4   4   3   3
-- cookie1   2015-04-13  3   5   5   4
-- cookie1   2015-04-14  2   6   6   5
-- cookie1   2015-04-10  1   7   7   6
```

#### 切片 (`NTILE`) TODO


#### 去重 (基于 `ROW_NUMBER`)
- 去重最常用的方法是使用 `GROUP BY`, 但有时不适用, 比如线上存在多个模型的结果, 我们需要最近出现次数最多的一个, 这时使用 `ROW_NUMBER` 更方便;

```sql
-- 场景: 对每个 query, 线上存在多个改写的结果, 现在需要取出最近最多的一个
SELECT *
FROM (
    SELECT *,
        ,  ROW_NUMBER() OVER(PARTITION BY query ORDER BY dt DESC, cnt DESC) AS rn
        -- 注意这里是 PARTITION BY query 而不是 PARTITION BY query, rewrite
    FROM (
        SELECT query, rewrite, dt, count(1) AS cnt
        FROM db.table
        WHERE dt > DATA_SUB('${env.today}', $DAYS)
        GROUP BY 1, 2, 3
    ) A
) A
WHERE rn = 1
```

#### 排序分位值
```sql
-- 场景：计算 query 的 pv 分位值
SELECT query
    , rn
    , 1.0 * acc_pv / sum_pv AS pr
    , pv
    , acc_pv
    , sum_pv
FROM (
    SELECT query
        , pv
        , ROW_NUMBER() OVER(ORDER BY pv desc) AS rn
        , SUM(pv) OVER() AS sum_pv
        , SUM(pv) OVER(ORDER BY pv desc ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as acc_pv
    FROM (
        SELECT stack(5,
            'A', 100,
            'B', 40,
            'C', 30,
            'D', 20,
            'E', 10
        ) AS (query, pv)
    ) A
) A
ORDER BY rn
;
--- result ---
query rn  pr    pv   acc_pv sum_pv
A     1   0.5   100  100    200
B     2   0.7   40   140    200
C     3   0.85  30   170    200
D     4   0.95  20   190    200
E     5   1.0   10   200    200
-- pr 列的含义: query A 占了 50% 的流量, A、B 占了 70% 的流量, ...
```


## 配置属性

### Hive
> [Configuration Properties - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/Configuration+Properties)

```sql
-- 使支持列位置别名, 即 GROUP/ORDER BY 1,2,3; 
SET hive.groupby.orderby.position.alias=true;  -- Deprecated In: Hive 2.2.0, 默认关闭
SET hive.groupby.position.alias=true;  -- Added In: Hive 2.2.0, 默认关闭
SET hive.orderby.position.alias=true;  -- Added In: Hive 2.2.0, 默认开启
```


## 其他

### `DISTINCT` 和 `GROUP BY` 在去重时有区别吗?
- 一些旧的经验会告诉你 `GROUP BY` 效率更高;
- 但是实际上两者的效率应该是一样的 (基于比较新的版本), 因为两者执行的步骤相同;
    > [sql - `distinct` vs `group by` which is better - Stack Overflow](https://stackoverflow.com/questions/31876137/distinct-vs-group-by-which-is-better/69929454#69929454) (来自2021年的回答)


### web 模板变量
- 如果公司提供了一个基于 Web 的 Hive 脚本编写平台, 那么一般都会支持这个功能;
- 下面以 [VTL (Velocity 模板语言)](https://wizardforcel.gitbooks.io/velocity-doc/content/5.html) 为例;
    ```sql
    #set( $day_delta = 60 );
    #set( $COND = 'A.pv > 10')

    SELECT *
    FROM db.table A
    WHERE A.dt > DATA_SUB('${today}', $day_delta)
    AND $COND
    ;  -- 注意这里 `$day_delta` 和 `$COND` 是 web 页面使用的变量; `${today}` 是 Hive 内部变量;
    ```

### 从 Hive 迁移到 Presto
> [Migrating From Hive — Presto Documentation](https://prestodb.io/docs/current/migration/from-hive.html)

下面记录区别较大的用法:
- Presto 中使用 `varchar` 代替 `string`;
- Presto 中数组下标从 1 开始, Hive 从 0 开始;
- Presto 中测试图关键字为 `CROSS JOIN`, Hive 中为 `LATERAL VIEW`, 详见 [侧视图 for Presto](#侧视图-for-presto-cross-join);
- Presto 中构造数组的语法 `array[1,2,3]`, Hive 中为 `array(1,2,3)`


## 异常记录

### 对 `f(col)` 分组或排序
> [GROUPing and SORTing on `f(column)` - Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF#LanguageManualUDF-GROUPingandSORTingonf(column))
```sql
SELECT lower(c) AS color, count(1) AS cnt
FROM (
    SELECT explode(ARRAY('red', 'red', 'RED', 'Red', 'Blue', 'blue')) AS c
) A
-- GROUP BY color   -- FAILED: Invalid Table Alias or Column Reference
GROUP BY lower(c)   -- OK
-- GROUP BY c       -- OK, 但不符合预期, 当 c 和 color 同名时非常容易犯这个错误
-- GROUP BY 1       -- OK, 需要 SET hive.groupby.position.alias=true;
```

### 日期加减
```sql
pt >  DATE_SUB('${env.today}', 7)  -- 7 天
pt >= DATE_SUB('${env.today}', 7)  -- 8 天
```

### `AS` 多个别名时要不要括号?
```sql
select explode(map('A',10,'B',20,'C',30)) as (key,value);  -- 必须要有括号
                                             ^^^^^^^^^^^
select tf.* from (select 0) t 
    lateral view explode(map('A',10,'B',20,'C',30)) tf as key,value;  -- 必须没有括号
                                                          ^^^^^^^^^
```

### 自动类型转换
- Hive 支持自动类型转换, 但是自动类型转换不一定会在所有你认为会发生的地方发生;
- 比如不支持将 `map<string, bigint>` 自动转换为 `map<string, double>`;
    ```sql
    INSERT ...
    SELECT map('a', 1, 
               'b', 2.0)  -- OK, 因为 2.0 的存在, 1 在插入时被自动转换为 double, 所以这是一个 map<string, double> 类型的值, 可以正常插入 map<string, double> 字段
        ...
    ;
    INSERT ...
    SELECT map('a', 1, 
               'b', 2)    -- err, 因为所有值都是 int, 所以这是一个 map<string, bigint> 类型的值, 把它插入到 map<string, double> 会报错;
    ``` 
- 解决方法: 使用 `CAST` 显式转换;


### 规避暴力扫描警告
- 在公共环境, 一般会限制单个查询扫描的数据量;
- 规避方法: 使用 `UNION ALL`
  ```sql
  SELECT ...
  FROM ...
  WHERE pt > ... AND pt <= ...

  UNION ALL

  SELECT ...
  FROM ...
  WHERE pt > ... AND pt <= ...
  ```