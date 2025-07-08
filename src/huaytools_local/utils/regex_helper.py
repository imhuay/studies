#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-15 19:12
Author:
    HuaYang(imhuay@163.com)
Subject:
    TODO
"""
import os
import re
import sys
import json
import doctest
import unicodedata

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

# third
import regex
import requests

# inner
from huaytools_local.utils._common import get_logger, get_cache_dir, get_resources_dir
from huaytools_local.utils._common import importlib_resources

logger = get_logger()

_PatternStr = Union[str, re.Pattern, regex.Pattern]
_Pattern = Union[re.Pattern, regex.Pattern]


class RegexEmoji:
    """
    References:
        - [Index of /Public/emoji](https://unicode.org/Public/emoji/)
        - [bsolomon1124/demoji](https://github.com/bsolomon1124/demoji)
    """
    _emojis: Dict = None
    _regex: re.Pattern = None
    _version: str = None

    # ClassVar
    _emoji_res_dir: ClassVar[Path] = get_resources_dir() / 'emojis'  # 默认保存路径
    _emoji_repo_url: ClassVar[str] = r'https://unicode.org/Public/emoji'
    _default_regex: ClassVar[re.Pattern] = None

    def __init__(self,
                 emoji_file_path: Union[str, Path] = None,
                 download: bool = False,
                 version: str = None):
        """
        Args:
            emoji_file_path: save or load emoji file path
            download: see https://unicode.org/Public/emoji/
        """
        self._download = download
        self._version = version or self._get_latest_version()
        if emoji_file_path is None:
            self._emoji_res_dir.mkdir(exist_ok=True)
            emoji_file_path = self._emoji_res_dir / f'{self._version}.txt'
        self._emoji_file_path = emoji_file_path

    def _download_and_save_emoji_file(self):
        """"""
        download_path = f'{self._emoji_repo_url}/{self._version}/emoji-test.txt'
        logger.info(f'Download emoji file from {download_path}')
        try:
            emoji_src = requests.get(download_path, stream=False, timeout=10)
        except requests.RequestException:
            logger.warning(f'Download emoji file from {download_path} Filed!')
        else:
            if emoji_src.status_code == 200:
                emoji_txt = emoji_src.content.decode('utf8')
                with open(self._emoji_file_path, 'w', encoding='utf8') as fw:
                    fw.write(emoji_txt)
            else:
                logger.warning(f'Some error when download from {download_path} '
                               f'with response.status_code={emoji_src.status_code}.')

    @staticmethod
    def _parse_unicode_sequence(s):
        return "".join(chr(int(i.zfill(8), 16)) for i in s.split())

    def _parse_emoji_file(self) -> dict:
        """"""
        emojis = dict()
        with open(self._emoji_file_path, encoding='utf8') as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith('#'):
                    continue
                _code, _desc = ln.split(';', 1)
                emoji_code = RegexEmoji._parse_unicode_sequence(_code.strip())
                _desc = _desc.split('#', 1)[1]
                _desc = _desc.split(' ', 3)[-1]
                emoji_desc = _desc.strip()
                emojis[emoji_code] = emoji_desc

        return emojis

    def _get_latest_version(self) -> str:
        """"""
        if self._download:  # 从仓库找最新版
            from bs4 import BeautifulSoup, Tag
            from huaytools_local.utils._common import get_response
            html = get_response(self._emoji_repo_url)
            soup = BeautifulSoup(html, features='html.parser')

            def tag_filter(tag: Tag):
                """
                <tr>..<img src="/icons/folder.gif" alt="[DIR]"></td><td><a href="1.0/">1.0/</a>..</tr>
                """
                if tag.name != 'a':
                    return False
                img = tag.parent.parent.img
                return img['alt'] == '[DIR]'

            tmp = [it.text[:-1] for it in soup.find_all(tag_filter)]
            tmp = sorted(tmp, key=lambda x: -float(x))
            return tmp[0]
        else:  # 从本地找最新版
            fs = [f.stem for f in self._emoji_res_dir.iterdir()]
            fs = sorted(fs, key=lambda x: -float(x))
            return fs[0]

    @property
    def emojis(self):
        if self._emojis is None:
            if self._download or not Path(self._emoji_file_path).exists():
                self._download_and_save_emoji_file()
            self._emojis = self._parse_emoji_file()
        return self._emojis

    @property
    def regex(self):
        if self._regex is None:
            emojis_unicode = [re.escape(e) for e in sorted(self.emojis, key=lambda x: -len(x))]
            self._regex = re.compile(r'|'.join(emojis_unicode))
        return self._regex

    @classmethod
    def get_default_regex(cls, **cls_kwargs):
        if cls._default_regex is None:
            cls._default_regex = cls(**cls_kwargs).regex
        return cls._default_regex


_RE_EMOJI: re.Pattern = RegexEmoji.get_default_regex()


class RegexUtils:

    @staticmethod
    def get_pattern_str(pat: _PatternStr):
        return pat if isinstance(pat, str) else pat.pattern

    @staticmethod
    def pat_exclude(wanted: _PatternStr,
                    exclude: _PatternStr) -> _Pattern:
        """
        匹配某个范围内的字符（如 [0-9]），但排除其中一部分（如 [3-5]）
        目前仅验证单个字符的匹配，不保证多个字符

        Examples:
            >>> r = RegexUtils.pat_exclude('[0-9]', '[3-5]')
            >>> assert r.match('4') is None
            >>> assert r.match('6') is not None
            >>> r = regex.compile('\\p{S}')
            >>> assert r.match('￥') is not None
            >>> r = RegexUtils.pat_exclude(regex.compile('\\p{S}'), '￥')
            >>> assert r.match('￥') is None
            >>> r = RegexUtils.pat_exclude(regex.compile('\\p{S}'), '[￥%]')
            >>> assert r.match('%') is None

        Args:
            wanted:
            exclude:

        Returns:

        """
        wanted = RegexUtils.get_pattern_str(wanted)
        exclude = RegexUtils.get_pattern_str(exclude)
        return regex.compile(rf'(?!{exclude}){wanted}')


class RegexLib:
    """
    Notes:
        # 如果不知道某个字符的 unicode 类型，可以使用 `unicodedata.category(c)` 查看
        >>> unicodedata.category('^')
        'Sk'

    References:
        - [re 模块 — Python 文档](https://docs.python.org/zh-cn/3/library/re.html)
        - [Unicode Character Database](https://www.unicode.org/reports/tr44/#General_Category_Values)
        - [Regex Tutorial - Unicode Characters and Properties](https://www.regular-expressions.info/unicode.html)
        - https://en.wikipedia.org/wiki/Unicode_block
        - https://en.wikipedia.org/wiki/CJK_Unified_Ideographs

    """
    # 连续多个 ASCII 空白字符，等价于 re.compile(r'[ \t\n\r\f\v]+')
    RE_ASCII_WHITESPACES = re.compile(r'\s+', flags=re.ASCII)
    # 连续多个空白字符，包括 UNICODE 字符
    RE_WHITESPACES = re.compile(r'\s+', flags=re.UNICODE)
    # 单个中文字符，包括繁体，中文标点等，覆盖 RE_CJK
    RE_HAN = regex.compile(r'\p{Han}')
    # 单个中文字符，ref: https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
    RE_CJK = re.compile(r'[\u4E00-\u9FFF]'  # CJK Unified Ideographs
                        '|[\uF900–\uFAFF]'  # CJK Compatibility Ideographs
                        '|[\U0002F800–\U0002FA1F]')  # CJK Compatibility Ideographs Supplement
    # 单个标点
    RE_PUNCTUATION = regex.compile(r'\p{P}')
    # 单个符号
    RE_SYMBOL = regex.compile(r'\p{S}')
    # 单个 Emoji 表情
    RE_EMOJI = _RE_EMOJI


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        doctest.testmod()

        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                v(self)

    def demo_xxx(self):
        """"""
        pass

    from huaytools_local.utils import function_timer

    @function_timer
    def demo_RegexEmoji(self):  # noqa
        """"""
        i = 0
        i += 1
        print(f'--- Test {i} ---')  # noqa
        r = RegexEmoji()
        print(list(r.emojis.items())[:3])

        i += 1
        print(f'--- Test {i} ---')  # noqa
        emoji_fp = r'/Users/huay/Workspace/my/studies/src/huaytools/_resources/emojis/13.1.txt'
        r = RegexEmoji(emoji_file_path=emoji_fp)
        print(list(r.emojis.items())[:3])

        i += 1
        print(f'--- Test {i} ---')  # noqa
        r = RegexEmoji(download=True)
        print(list(r.emojis.items())[:3])

        i += 1
        print(f'--- Test {i} ---')  # noqa
        try:
            r = RegexEmoji(version='0.0')
            print(list(r.emojis.items())[:3])
        except:  # noqa
            print('No such version.')

        i += 1
        print(f'--- Test {i} ---')  # noqa
        r = RegexEmoji(version='12.0')
        print(list(r.emojis.items())[:3])

        i += 1
        print(f'--- Test {i} ---')  # noqa
        r = RegexEmoji(version='12.0')
        print(list(r.emojis.items())[:3])

        i += 1
        print(f'--- Test {i} ---')  # noqa
        r = RegexEmoji.get_default_regex()
        r2 = RegexEmoji.get_default_regex()
        print(r is r2 is _RE_EMOJI)
        print(_RE_EMOJI.sub(' ', "a😀😃b c😄c"))


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
