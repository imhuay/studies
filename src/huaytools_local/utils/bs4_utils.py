#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-22 01:08
Author:
    HuaYang(imhuay@163.com)
Subject:
    Utils for BeautifulSoup
"""
import os
import sys
import json
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

from bs4 import BeautifulSoup, Tag

from huaytools_local.utils._common import get_logger

_logger = get_logger()


class BS4Utils:
    """"""

    @staticmethod
    def get_html_soup(url: str, features='html.parser', **soup_kwargs) -> BeautifulSoup:
        from huaytools_local.utils._common import get_response
        html = get_response(url)
        soup = BeautifulSoup(html, features=features, **soup_kwargs)
        return soup

    @staticmethod
    def find_previous(tag: Tag, tag_name, count=1):
        """"""
        while count:
            tag = tag.previous
            if tag is None:
                _logger.info(f'No {tag_name} before current {tag.name}.')
                break
            if tag.name == tag_name:
                count -= 1

        return tag


class _BS4Wrap:
    """"""

    def __init__(self, src: Union[BeautifulSoup, str]):
        """"""
        if isinstance(src, BeautifulSoup):
            self.soup = src
        else:
            self.soup = BS4Utils.get_html_soup(src)


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        doctest.testmod()

        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                v(self)

    def demo_base(self):  # noqa
        """"""
        url = r'https://www.google.com'
        soup = BS4Utils.get_html_soup(url)

        tag = soup.find_previous()
        print(tag)


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
