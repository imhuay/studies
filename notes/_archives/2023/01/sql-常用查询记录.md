Hive/Spark SQL 常用查询记录
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: true
-->

> ***Keywords**: Hive/Spark SQL*

<!--START_SECTION:toc-->
<!--END_SECTION:toc-->
<!-- > [*References*](#References) -->

## 聚合操作

### 


## 个人习惯

### 集合字段 `map/json`
- 作为一个额外字段, 可以把新的字段统一放到这里, 防止频繁修改表;
    <!-- - 主要是 `bigint/double/string` 类型的字段, 其他集合类型, 建议转成 `string`; -->
<!-- - 数值类型可以放到 `features map < string, double > COMMENT '数值类型 features'`,  -->

```sql
-- CREATE
CREATE TABLE db.table (
    ...
    , `features`    map < string, double >  COMMENT 'features'
    , `info_json`   string                  COMMENT 'extra info'
) COMMENT 'xxx 特征表'

-- INSERT

INSERT OVERWRITE TABLE db.table
SELECT ...
    , map(
          'f1', f1_double
        , 'f2', f2_int
        , ...
      ) AS features
    , concat('{'
        , '"k1":', k1_int, ','  -- 注意 key 要双引号
        , '"k2":', k2
      , '}') AS info_json
FROM ...

-- SELECT
SELECT ...
    ,  features['f1'] AS f1
    ,  features['f2'] AS f2
    ,  get_json_object(info_json, '$.k1') AS k1
    ,  get_json_object(info_json, '$.k2') AS k2
FROM db.table
```


### 小词表
```sql

```