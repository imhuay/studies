SQL 字符串处理
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [参考文档](#参考文档)
- [常规](#常规)
    - [小写](#小写)
    - [移除首尾空白符](#移除首尾空白符)
    - [拼接](#拼接)
    - [截取](#截取)
- [正则](#正则)
    - [正则替换](#正则替换)
    - [正则切分](#正则切分)
    - [正则抽取](#正则抽取)

## 参考文档
- [Presto Documentation](https://prestodb.io/docs/current/)

## 常规

### 小写
`lower(string)`
- 支持的引擎：
    - [Presto](https://prestodb.io/docs/current/functions/string.html#lower)
- 对应的 Python 操作：`str.lower()`

### 移除首尾空白符
`trim(string)`
- 支持的引擎：
    - [Presto](https://prestodb.io/docs/current/functions/string.html#trim)
- 对应的 Python 操作：`str.strip()`

### 拼接
`array_join(array, sep, null_replacement)`
- 支持的引擎：
    - [Presto](https://prestodb.io/docs/current/functions/array.html#array_join)
        ```sql
        SELECT array_join(ARRAY[1, NULL, 2], ','); -- 1,2
        SELECT array_join(ARRAY[1, NULL, 2], '_', 'N'); -- 1_N_2
        SELECT array_join(
                    regexp_split('a(b), c', '[^a-z]'), 
                    ' ');  -- 'a b c'
        ```
- 对应的 Python 操作：`sep.join(array)`

### 截取
- `substr(string, start)`
- `substr(string, start, length)`
    > [substr - Presto](https://prestodb.io/docs/current/functions/string.html#substr)
    >> 注意：Positions start with 1
    ```sql
    -- Presto
    SELECT substr('abcde', 1)   -- abcde
    , substr('abcde', 2)        -- bcde
    , substr('abcde', 2, 3)     -- bcd
    , substr('abcde', -2)       -- de
    , substr('abcde', -3, 2)    -- cd
    ;
    ```


## 正则

### 正则替换
- `regexp_replace(string, pattern, replacement)`
    > [regexp_replace - Presto](https://prestodb.io/docs/current/functions/regexp.html#regexp_replace)
    ```sql
    -- Presto
    SELECT regexp_replace('a   b  c', '\s+', ' '); -- 'a b c'
    ```

### 正则切分
- `regexp_split(string, pattern)`
    > [regexp_split - Presto](https://prestodb.io/docs/current/functions/regexp.html#regexp_split)
    ```sql
    -- Presto
    SELECT regexp_split('a(b), c', '[^a-z]'); -- '[a, b, , , c]'
    SELECT array_join(
                regexp_split('a(b), c', '[^a-z]'), 
                ' ');  -- 'a b c'
    ``` 

### 正则抽取
- `regexp_extract(string, pattern)`
- `regexp_extract(string, pattern, group)`
    > [regexp_extract - Presto](https://prestodb.io/docs/current/functions/regexp.html#regexp_extract)
    ```sql
    -- Presto
    SELECT regexp_extract('1a 2b 14m', '\d+'); -- 1
    SELECT regexp_extract('1a 2b 14m', '(\d+)([a-z]+)', 2); -- 'a'
    ```
- `regexp_extract_all(string, pattern)`
- `regexp_extract_all(string, pattern, group)`
    > [regexp_extract_all - Presto](https://prestodb.io/docs/current/functions/regexp.html#regexp_extract_all)
    ```sql
    -- Presto
    SELECT regexp_extract_all('1a 2b 14m', '\d+'); -- [1, 2, 14]
    SELECT regexp_extract_all('1a 2b 14m', '(\d+)([a-z]+)', 2); -- ['a', 'b', 'm']
    ```