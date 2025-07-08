PySpark 笔记
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

<!-- TOC -->
- [环境设置](#环境设置)
    - [Python 依赖管理](#python-依赖管理)
<!-- TOC -->


## 环境设置

### Python 依赖管理
> [How to Manage Python Dependencies in Spark - The Databricks Blog](https://www.databricks.com/blog/2020/12/22/how-to-manage-python-dependencies-in-pyspark.html)
```shell
# 基于 conda
# 进入需要打包的 conda 环境
conda activate my_pyspark

# 安装 conda-pack, 使用 -c conda-forge 安装最新版本
conda install conda-pack -c conda-forge

# 打包当前环境, -f 表示强制覆盖已存在的文件
conda-pack -f -o my_pyspark.tar.gz

# 打包指定环境
conda-pack -f -n some_env -o some_env.tar.gz
```
> 注意使用 `conda-pack` 而不是 `conda pack`, 否则可能会不兼容 python3.10+
>> [Conda pack does not work with Python 3.10 or 3.11 · Issue #244 · conda/conda-pack](https://github.com/conda/conda-pack/issues/244)