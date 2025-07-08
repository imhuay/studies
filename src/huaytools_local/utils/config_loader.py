#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-01 7:23 下午
    
Author:
    huayang
    
Subject:
    一个用于加载配置文件的装饰器，参考自开源库 hydra，其中的一种典型的使用场景。
    ```
    import hydra

    @hydra.main("config.yaml")
    def main(cfg):
        ...
    ```

References:
    facebookresearch/hydra | https://github.com/facebookresearch/hydra
"""
import os
import sys
import json
import functools

from huaytools_local.utils.dict_extensions import BunchDict
from huaytools_local.utils._common import get_logger

_logger = get_logger()
ALLOW_FILE_TYPE = {'json', 'yaml'}


def _load_config_json(config_path):
    with open(config_path) as fp:
        config = json.load(fp)
    return config


def _load_config_yaml(config_path):
    try:
        import yaml
    except ImportError:
        raise ImportError('No `yaml` module, please `pip install pyyaml`.')

    with open(config_path) as fp:
        config = yaml.safe_load(fp.read())
    return config


def load_config_file(file_path=None, file_type=None, bunching=True, cls=None):
    """"""
    if file_path is None:  # 从命令行提取
        if len(sys.argv) < 2:
            raise ValueError('Config file path must be given, using parameter or command line.')
        file_path = sys.argv[1]

    if file_type is None:  # 看后缀文件
        _, ext = os.path.splitext(file_path)
        file_type = ext[1:]

    if file_type == 'json':
        cfg = _load_config_json(file_path)
    elif file_type in ('yaml', 'yml'):
        cfg = _load_config_yaml(file_path)
    else:
        raise ValueError('Error file_type: "%s"' % (file_type,))

    bunching = bunching if cls is None else False
    if bunching:
        cfg = BunchDict.from_dict(cfg)

    if cls is not None:
        # assert issubclass(cls, BaseConfig)
        cfg = cls(**cfg)

    return cfg


def load_config(file_path=None, file_type=None, config_cls=None):
    """
    配置文件加载装饰器
    
    Args:
        file_path: 
        file_type: 
        config_cls: 
        
    Examples:
        # 场景 1：显示指定配置文件位置
        @load_config('_test/test_config.json')
        def main(cfg):
            print(cfg.a)
            print(cfg.b)
            print(cfg.c.d)  # 可以直接点取二级参数
        
        # 场景 2：在命令行确定文件位置
        @load_config()
        def main(cfg):
            print(cfg.a)
            print(cfg.b)
            print(cfg.c.d)  # 可以直接点取二级参数
        
        > python xxx.py _test/test_config.yaml
        
        # 场景 3: 自定义配置类，优点是有提示，缺点是二级参数只能通过字典方式提取
        class TestConfig(BaseConfig):
            def __init__(self, **kwargs):
                self.a = None
                self.b = None
                self.c = None
                super(TestConfig, self).__init__(**kwargs)
        
        @load_config('_test/test_config.json', config_cls=TestConfig)
        def main(cfg):
            print(cfg.a)
            print(cfg.b)
            print(cfg.c['d'])  # 二级参数只能用字典方式提取
    """

    def main_decorator(func):
        """"""

        @functools.wraps(func)
        def decorated_func():
            """"""
            cfg = load_config_file(file_path, file_type, bunching=True, cls=config_cls)
            # if config_cls is None:
            #     cfg = Bunch.from_dict(cfg)
            # else:
            #     cfg = config_cls(**cfg)
            func(cfg)

        return decorated_func

    return main_decorator


def _test():
    """"""

    def _test_load_config_file():
        """"""
        file_path = r'_test_data/test_config.yaml'
        cfg = load_config_file(file_path, bunching=False)
        assert isinstance(cfg, dict)
        assert cfg == {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}

        cfg = load_config_file(file_path)
        assert isinstance(cfg, BunchDict)

    _test_load_config_file()

    def _test_load_config():
        @load_config()
        def main1(cfg):
            """"""
            assert cfg.a == 1
            assert cfg.b == {'c': 2, 'd': {'e': 3}}
            assert cfg.b.c == 2
            assert cfg == {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}

        @load_config('_test_data/test_config.yaml', file_type='yaml')
        def main2(cfg):
            """"""
            assert cfg.a == 1
            assert cfg.b == {'c': 2, 'd': {'e': 3}}
            assert cfg.b.c == 2
            assert cfg == {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}

        sys.argv = ['', './_test_data/test_config.json']
        main1()
        main2()

    _test_load_config()


if __name__ == '__main__':
    """"""
    _test()
