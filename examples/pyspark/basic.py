#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-11 14:41
Author:
    HuaYang(imhuay@163.com)
Subject:
    Spark 任务模板
"""
# import os
# import sys
# import json

# from collections import defaultdict

from huaytools_local.pyspark import *


class SparkTaskTemplate:
    """
    Attributes:
        df_rdd: 通过 SQL 查询到的 RDD
        final_rdd: 最终处理完成的 RDD
    """
    df: DataFrame
    df_rdd: RDD[Row]
    final_rdd: RDD

    @property
    def sql(self):
        """"""
        # _TODO
        return self._sql or '''
        SELECT *
        FROM some_table
        '''

    def process(self):
        """具体的处理逻辑"""
        rdd = self.df_rdd
        # _TODO

        self.final_rdd = ...

    def __init__(self,
                 local_file_path: str = None,
                 *,
                 sql: str = None,
                 save_path: str = None,
                 save_type: str = 'csv',
                 save_to_hive: bool = True,
                 spark: SparkSession = None):
        """

        Args:
            local_file_path: 本地文件是通过 sql 查询出来的内容（部分），用于本地测试
            sql: 用于查询数据的 Spark SQL
            save_path: 保存路径；若为 None 按如下逻辑设置：
                本地测试默认保存在当前目录下的 data 文件夹，文件名与 py 文件同名；
                远程默认保存路径为 hdfs 路径；
                若 save_to_hive 为 True，
            save_type: one of {'csv', 'txt', 'json'}
            save_to_hive:
            spark:
        """
        self.local_fp = local_file_path
        self._sql = sql
        self._save_path = save_path
        self.save_type = save_type
        self.save_to_hive = save_to_hive
        self.spark = SparkUtils.get_spark(spark)

        self.load_df_and_rdd()
        self.process()
        self.save()

    def load_df_and_rdd(self):
        if SparkUtils.is_local():
            local_kw = {}
            df = SparkUtils.load_csv(self.local_fp, spark=self.spark, **local_kw)
        else:
            df = self.spark.sql(self.sql)
        self.df = df
        self.df_rdd = df.rdd

    def save(self):
        """"""
        rdd = self.final_rdd
        # TODO
        if SparkUtils.is_local():
            # save to file(csv or text)
            pass
        else:
            # save to file or hive
            pass
            if self.save_to_hive:
                pass

    @property
    def save_path(self):
        """"""
        if self._save_path is not None:
            return self._save_path

        name = Path(__file__).stem
        if SparkUtils.is_local():
            save_path = rf'./data/{name}.{self.save_type}'
        else:
            if self.save_to_hive:
                save_path = name
            else:
                raise ValueError(r'some hdfs path')
        return save_path


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        import doctest
        doctest.testmod()

        # self.demo_load_csv()
        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                v(self)

    def demo_local(self):  # noqa
        """"""
        local_file_path = r''
        task = SparkTaskTemplate(local_file_path)


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
