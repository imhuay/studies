#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-12 15:04
Author:
    HuaYang(yang.hua@shopee.com)
Subject:
    PySpark Utils
"""
import logging
from typing import *
from pathlib import Path

from pyspark import RDD
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame, DataFrameReader
from pyspark.sql import Row
from pyspark.sql.types import StructType

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.WARNING)


class SparkUtils:
    """"""
    logger = logging.getLogger('SparkUtils')

    @staticmethod
    def is_local():
        """"""
        import platform
        return platform.system() != 'Linux'

    @staticmethod
    def get_spark_and_sc(app_name='huayang_spark',
                         master: str = None,
                         enable_hive_support: bool = True,
                         log_level: str = 'WARN',
                         config: Dict[str, Any] = None):
        """"""
        builder = SparkSession.builder.appName(app_name)
        if enable_hive_support:
            # builder = builder.enableHiveSupport()
            builder.config("spark.sql.catalogImplementation", "hive")
        if master is not None:
            # builder = builder.master(master)
            builder.config("spark.master", master)
        if config is None:
            config = dict()
        if SparkUtils.is_local():
            config.setdefault('spark.driver.bindAddress', '127.0.0.1')
        for k, v in config.items():
            builder.config(k, v)

        spark = builder.getOrCreate()
        sc = spark.sparkContext
        sc.setLogLevel(log_level)
        return spark, sc

    @staticmethod
    def get_spark(spark: SparkSession = None) -> SparkSession:
        if spark is not None:
            return spark
        spark = SparkSession.getActiveSession()
        if spark is None:
            spark, _ = SparkUtils.get_spark_and_sc()
        return spark

    @staticmethod
    def get_reader(spark: SparkSession, schema: Union[StructType, str] = None) -> DataFrameReader:
        return spark.read if schema is None else spark.read.schema(schema)

    @staticmethod
    def load(src: Union[str, List[str]],
             src_format: str = None,
             spark: SparkSession = None,
             schema: Union[str, StructType] = None,
             **format_options) -> DataFrame:
        """

        Args:
            src:
            src_format: one of {'text', 'csv', 'json', 'orc', 'parquet'}
            schema:
            spark:
            **format_options:

        Examples:
            > schema = 'name STRING, age INT'
            > load_file(spark, src, src_type='text', schema=schema, lineSep=line_sep, **options)
            > load_file(spark, src, src_type='csv', header=True, sep=',', quote='"', infer_schema=True, **options)

        See Also:
            `load_csv`
            `load_txt`
        """
        spark = SparkUtils.get_spark(spark)
        if src_format is None:
            src_format = Path(src).suffix[1:]
            if src_format == 'txt':
                src_format = 'text'
        reader = spark.read.format(src_format).options(**format_options)
        df = reader.load(src, schema=schema)
        return df

    @staticmethod
    def load_csv(src: Union[str, List[str]],
                 spark: SparkSession = None,
                 schema: Union[StructType, str] = None,
                 header=True, sep=',', quote='"', infer_schema=True, **options) -> DataFrame:
        """

        Args:
            src:
            spark:
            schema:
            header:
            sep:
            quote:
            infer_schema:
            **options:

        Returns:

        """
        reader = SparkUtils.get_spark(spark).read
        df = reader.csv(src, schema=schema, header=header, sep=sep, quote=quote, inferSchema=infer_schema, **options)
        return df

    @staticmethod
    def load_txt(src: Union[str, List[str]],
                 spark: SparkSession = None,
                 line_sep=None, **options) -> DataFrame:
        """
        Notes:
            对 txt 文件，只能按一列读取，默认列名为 value，且类型只能为 STRING；
            如果需要处理为多列，只能
                1. 加载后通过 df.map() 处理；
                2. 或者当做 csv 文件处理（指定分隔符）

        Args:
            src:
            spark:
            line_sep: 行分隔符
            **options:

        Returns:

        """
        reader = SparkUtils.get_spark(spark).read
        df = reader.text(src, lineSep=line_sep, **options)
        return df

    @staticmethod
    def save(rdd: RDD,
             save_path: str,
             save_format: str = 'csv',
             mode: str = 'overwrite',
             partition: Union[str, List[str]] = None,
             spark: SparkSession = None,
             schema: Union[StructType, str] = None,
             **format_options):
        """"""
        spark = SparkUtils.get_spark(spark)
        df = spark.createDataFrame(rdd, schema=schema)
        writer = df.write.format(save_format).options(**format_options)
        writer.save(save_path, mode=mode, partitionBy=partition)

    @staticmethod
    def save_to_csv(rdd: RDD,
                    save_dir: str,
                    mode: str = 'overwrite',
                    save_to_one_file: bool = False,
                    delete_src: bool = True,
                    header: bool = True,
                    sep: str = ',',
                    quote: str = '"',
                    quote_all: bool = True,
                    spark: SparkSession = None,
                    schema: Union[StructType, str] = None,
                    **options):
        """"""
        spark = SparkUtils.get_spark(spark)
        df = spark.createDataFrame(rdd, schema=schema)
        df.write.csv(save_dir, mode=mode,
                     header=header, sep=sep, quote=quote, quoteAll=quote_all, **options)
        if save_to_one_file:
            save_path = rf'{save_dir}.csv'
            SparkUtils.save_to_one_file(save_dir, save_path, delete_src=delete_src)

    @staticmethod
    def save_to_txt(rdd: RDD,
                    save_dir: str,
                    save_to_one_file: bool = False,
                    delete_src: bool = True,
                    line_sep: str = None,
                    compression: str = None,
                    spark: SparkSession = None,
                    schema: Union[StructType, str] = None):
        spark = SparkUtils.get_spark(spark)
        df = spark.createDataFrame(rdd, schema=schema)
        df.write.text(save_dir, lineSep=line_sep, compression=compression)
        if save_to_one_file:
            save_path = rf'{save_dir}.txt'
            SparkUtils.save_to_one_file(save_dir, save_path, delete_src=delete_src)

    @staticmethod
    def save_to_one_file(src_dir, save_path, delete_src,
                         src_prefix='part', spark: SparkSession = None):
        """"""
        if SparkUtils.get_spark_submit_deploy_mode(spark) != 'client':
            SparkUtils.logger.warning(f'`save_to_one_file` is effective only when spark deploy mode is client')
        else:
            import os
            os.system(f'cat {src_dir}/{src_prefix}* > {save_path}')
            if delete_src:
                os.system(f'rm -rf {src_dir}')

    @staticmethod
    def get_spark_submit_deploy_mode(spark: SparkSession = None):
        """"""
        return SparkUtils.get_spark(spark).conf.get('spark.submit.deployMode')


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        import doctest
        doctest.testmod()
        spark = SparkUtils.get_spark()
        print()
        print(spark.conf.get("spark.submit.deployMode"))

        # self.demo_load_csv()
        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                v(self)

    def demo_load_and_save_csv(self):  # noqa
        """"""
        # load
        fp = r'./_demo/data.csv'
        schema = 'name STRING, age INT'
        df = SparkUtils.load_csv(fp, header=True, schema=schema, infer_schema=False)
        print(df.schema)
        df.show()

        # process
        rdd = df.rdd.map(lambda row: row.name) \
            .flatMap(lambda name: name.split()) \
            .map(lambda word: [word, 1])

        # save
        fw = r'./_demo/out'
        schema = "word STRING, cnt INT"
        SparkUtils.save_to_csv(rdd, fw, schema=schema, save_to_one_file=True)

    def demo_load_and_save_txt(self):  # noqa
        """"""
        # load
        fp = r'./_demo/data.txt'
        df = SparkUtils.load_txt(fp)
        print(df.schema)
        df.show()

        # process
        rdd = df.rdd.map(lambda row: row.value) \
            .flatMap(lambda name: name.split()) \
            .map(lambda word: [f'{word} 1'])

        # save
        fw = r'./_demo/out'
        SparkUtils.save_to_txt(rdd, fw, save_to_one_file=True)


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
