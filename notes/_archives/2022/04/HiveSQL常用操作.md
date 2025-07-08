Hive SQL 常用操作
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [正则](#正则)
    - [常用正则](#常用正则)
- [常用参数](#常用参数)
- [窗口函数-排序](#窗口函数-排序)
- [分段采样](#分段采样)
- [`case when` 基本用法](#case-when-基本用法)
- [加载自定义 UDF](#加载自定义-udf)
- [加载 transform](#加载-transform)
    - [临时 pip 模块](#临时-pip-模块)
    - [添加额外参数来选择调用函数](#添加额外参数来选择调用函数)
- [临时表](#临时表)
- [建表](#建表)
- [加载 hdfs 数据](#加载-hdfs-数据)
- [查看表信息](#查看表信息)

## 正则
> Java 正则表达式 | 菜鸟教程 | https://www.runoob.com/java/java-regular-expressions.html

### 常用正则
```
中文：[\\u4E00-\\u9FA5]
2字以上中文： '^[\\u4E00-\\u9FA5]{2,}$'
ASCII 可见字符 & 标准中文字符集：[\\x21-\\x7e\\u4E00-\\u9FA5]
```


## 常用参数
```sql
-- hive 引擎
SET mapred.reduce.tasks=64;
SET mapred.max.split.size=1024000;          -- 决定每个map处理的最大的文档大小，单位为B，越小 map 越多
SET mapred.min.split.size.per.node=512000;  -- 节点中可以处理的最小的文档大小（可以考虑设置为 max 的一半）
SET mapred.min.split.size.per.rack=512000;  -- 机架中可以处理的最小的文档大小（与 node 相同）
SET mapreduce.map.memory.mb=8192;
SET mapreduce.reduce.memory.mb=8192;

-- spark 引擎
SET spark.executor.memory=10G;
```


## 窗口函数-排序
> HIVE SQL奇技淫巧 - 知乎 | https://zhuanlan.zhihu.com/p/80887746
```sql
SELECT 
    cookieid,
    createtime,
    pv,
    RANK() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn1,         -- 1,1,3,3,5
    DENSE_RANK() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn2,   -- 1,1,2,2,3
    ROW_NUMBER() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn3    -- 1,2,3,4,5
    NTILE(4) OVER(ORDER BY pv) AS rn4  --将所有数据分成4片
FROM lxw1234 
WHERE cookieid = 'cookie1';

cookieid day           pv       rn1     rn2     rn3     rn4 
----------------------------------------------------------- 
cookie1 2015-04-12      7       1       1       1       1
cookie1 2015-04-11      5       2       2       2       1
cookie1 2015-04-15      4       3       3       3       2
cookie1 2015-04-16      4       3       3       4       2
cookie1 2015-04-13      3       5       4       5       3
cookie1 2015-04-14      2       6       5       6       3
cookie1 2015-04-10      1       7       6       7       4
```


## 分段采样
```sql
-- 有类别标签
SELECT query, label
FROM (
    SELECT query, label
        , row_number() over(partition by label order by rand()) row_num  -- 打乱每堆内部
    FROM some_table
) A
WHERE row_num <= 300  -- 每堆采样 300 条

-- 无类别标签
SELECT query, qv, heap
FROM (
    SELECT query, qv, heap, row_number() over(partition by heap order by rand()) row_num  -- 打乱每堆内部
    FROM (
        SELECT query, qv, ntile(10) over(order by qv desc) AS heap  -- 按 qv 降序分成 10 堆
        FROM table_query_qv
    ) A
) B
WHERE row_num <= 300  -- 每堆采样 300 条
;
```


<!-- ## 获取星期
```sql
pmod(datediff('#data#', '2012-01-01'), 7)  -- 返回 0-6 表示 星期日-星期六
``` -->


## 行转列、侧视图
```sql
-- hive
LATERAL VIEW EXPLODE(split(sstr,'\\|')) X AS sth  -- `|` 需要转义
LATERAL VIEW EXPLODE(mentionlist) X AS mention
LATERAL VIEW EXPLODE(array(1,2,3,4)) X AS i

-- presto
CROSS JOIN UNNEST(arr1) AS T (a1)  -- unzip
CROSS JOIN UNNEST(split(label_id, '|')) AS T (iid)  -- presto 环境下 `|` 不需要转义
CROSS JOIN UNNEST(arr1, arr2) AS T (a1, a2)  -- unzip

```

## `case when` 基本用法
```
case 
    when RequestInfo like '%mtMerger%' and source='2' then 'mt'
    when source = '1' then 'mt'
    when source = '3' then 'other' 
    else 'dp' 
end
```

## 加载自定义 UDF
```
-- 加载 jar 包
add jar viewfs:///path/of/some.jar;
-- 创建函数
CREATE TEMPORARY FUNCTION func_name AS 'package.path.of.SomeUDF';
```

## 加载 transform
```
add file $Script('xxx.py');

transform ()
using '/usr/bin/python2.7 xxx.py'
as ()
```

### 临时 pip 模块
```python
# print(os.getcwd())
tmp_dir = './tmp_dir'
os.mkdir(tmp_dir)
sys.stdout = open(os.devnull, 'w+')  # 输出重定向，防止 pip 的信息输出到 hive 表中
pip.main(['install', 'pypinyin', '-t', tmp_dir, '--ignore-installed'])  # -t 表示安装到指定位置
sys.path.append(tmp_dir)  # 添加环境变量
sys.stdout = sys.__stdout__  # 还原输出重定向

import pypinyin
# run()

pip.main(['uninstall', 'pypinyin', '-y'])  # -y 表示直接确认
shutil.rmtree(tmp_dir)
```

### 添加额外参数来选择调用函数
```python
# 调用方式：
## using '/usr/bin/python2.7 xxx.py --a'

if len(sys.argv) <= 1:
    raise Exception('--a or --b must be set')
args = tuple(sys.argv[2:])
if sys.argv[1] == '--a':
    run_a()
elif sys.argv[1] == '--b':
    run_b()
```


## 临时表
```sql
-- 上线时使用（Hive 环境下不支持）
#set $table_name = 'tmp_子表名';
CACHE TABLE $table_name AS
;

-- 测试时使用
DROP TABLE IF EXISTS `${tmpdb}`.tmphuay_子表名;
CREATE TABLE `${tmpdb}`.tmphuay_子表名 AS
;

-- 不写建表语句
DROP TABLE IF EXISTS `${target.table}`;
CREATE TABLE `${target.table}` STORED AS ORC AS
;
```

## 建表
```sql
CREATE TABLE IF NOT EXISTS `$target.table`
(
    `entityID` string COMMENT 'entityID',
    `sequence` string COMMENT 'sequence'
)
COMMENT ''
PARTITIONED BY (hp_stat_date string comment '天分区，yyyy-mm-dd')
ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t'
    LINES TERMINATED BY '\n'
STORED AS textfile
-- STORED AS ORC
-- LOCATION "/user/hadoop-aipnlp/entitylink_entity";
```


## 加载 hdfs 数据
```sql
LOAD DATA INPATH 'viewfs://hadoop-meituan/user/hadoop-aipnlp/huayang04/el_trm/pred__a__b__all.txt'
OVERWRITE into table `${tmpdb}`.tmphuay_entitylink_trm_sample_bert_feature__a__b__tmp;
```

## 查看表信息
```sql
show create table `table_name`
```