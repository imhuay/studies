基于 SQL 计算信息熵与信息增益
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: SQL, 信息熵 (Information Entropy)，信息增益 (相对熵, KL 散度)*

<!--START_SECTION:toc-->
<!--END_SECTION:toc-->
<!-- > [*References*](#References) -->

## 参考资料
- [一条SQL搞定信息增益的计算 - 腾讯云开发者 - 博客园](https://www.cnblogs.com/qcloud1001/p/6735352.html)


## 测试数据
```sql
SELECT inline(array(
    struct(1,  'boy',   'high',     0),
    struct(2,  'girl',  'medium',   0),
    struct(3,  'boy',   'low',      1),
    struct(4,  'girl',  'high',     0),
    struct(5,  'boy',   'high',     0),
    struct(6,  'boy',   'medium',   0),
    struct(7,  'boy',   'medium',   1),
    struct(8,  'girl',  'medium',   0),
    struct(9,  'girl',  'low',      1),
    struct(10, 'girl',  'medium',   0),
    struct(11, 'girl',  'high',     0),
    struct(12, 'boy',   'low',      1),
    struct(13, 'girl',  'low',      1),
    struct(14, 'boy',   'high',     0),
    struct(15, 'boy',   'high',     0)
)) AS (uid, gender, act_info, is_lost)
```
- 第一列为用户 ID，第二列为性别，第三列为活跃度，最后一列用户是否流失。
- 问题：性别和活跃度两个特征，哪个对用户流失影响更大？

## 计算

### 特征转置
```sql
SELECT A.uid, B.feature_name, B.feature_value, A.is_lost 
FROM (
    SELECT inline(array(
        struct(1, 'boy', 'high', 0),
        struct(2, 'girl', 'medium', 0),
        struct(3, 'boy', 'low', 1),
        struct(4, 'girl', 'high', 0),
        struct(5, 'boy', 'high', 0),
        struct(6, 'boy', 'medium', 0),
        struct(7, 'boy', 'medium', 1),
        struct(8, 'girl', 'medium', 0),
        struct(9, 'girl', 'low', 1),
        struct(10, 'girl', 'medium', 0),
        struct(11, 'girl', 'high', 0),
        struct(12, 'boy', 'low', 1),
        struct(13, 'girl', 'low', 1),
        struct(14, 'boy', 'high', 0),
        struct(15, 'boy', 'high', 0)
    )) AS (uid, gender, act_info, is_lost)
) A
LATERAL VIEW explode(map('gender', A.gender, 'act_info', A.act_info)) B AS feature_name, feature_value

-- ret
uid feature_name feature_value is_lost
1     gender      boy       0
2     gender      girl      0
3     gender      boy       1
4     gender      girl      0
5     gender      boy       0
6     gender      boy       0
7     gender      boy       1
8     gender      girl      0
9     gender      girl      1
10    gender      girl      0
11    gender      girl      0
12    gender      boy       1
13    gender      girl      1
14    gender      boy       0
15    gender      boy       0
1     act_info    high      0
2     act_info    medium    0
3     act_info    low       1
4     act_info    high      0
5     act_info    high      0
6     act_info    medium    0
7     act_info    medium    1
8     act_info    medium    0
9     act_info    low       1
10    act_info    medium    0
11    act_info    high      0
12    act_info    low       1
13    act_info    low       1
14    act_info    high      0
15    act_info    high      0
```

### 特征统计/计数
```sql

```