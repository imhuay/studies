#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-27 15:46
Author:
    HuaYang (imhuay@163.com)
Subject:
    Normalize Utils for NLP
"""
import os
import re
import sys
import json
import time
import unicodedata

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict


class NormalizeUtils:
    """"""
    RE_EMOJI: ClassVar[re.Pattern] = None

    @staticmethod
    def untie_ligatures(seq: str):
        """
        Untie ligatures.
        Note that not all ligatures can be untied, such as "ꜳ, æ, ..."

        Args:
            seq:

        Examples:
            >>> txt = 'Ligature examples: ﬁ, ﬀ, ﬃ, ꜳ'
            >>> NormalizeUtils.untie_ligatures(txt)
            'Ligature examples: fi, ff, ffi, ꜳ'

        References:
            https://en.wikipedia.org/wiki/Ligature_(writing)
        """
        return unicodedata.normalize('NFKD', seq)

    @staticmethod
    def remove_emojis(seq: str, repl=' ') -> str:
        """
        Remove emojis from a text sequence.

        Args:
            seq:
            repl: replace emoji by `repl`, default one space

        Examples:
            >>> txt = r'A text with some emojis: 😉, 😂, 😊.'
            >>> NormalizeUtils.remove_emojis(txt)
            'A text with some emojis:  ,  ,  .'
        """
        if NormalizeUtils.RE_EMOJI is None:
            from huaytools_local.utils.regex_helper import RegexEmoji
            NormalizeUtils.RE_EMOJI = RegexEmoji.get_default_regex()

        seq = NormalizeUtils.RE_EMOJI.sub(repl, seq)
        return seq

    @staticmethod
    def remove_accents(seq, form='NFD') -> str:
        """
        Remove accents from a char sequence.

        Args:
            seq:
            form: 'NFD' or 'NFKD', suggest 'NFD';
                'NFD' just remove the accents, 'NFKD' may change the char ('ﬁ' -> 'fi')

        Examples:
            >>> _s = 'âbĉ'
            >>> NormalizeUtils.remove_accents(_s)
            'abc'
        """
        seq = unicodedata.normalize(form, seq)
        output = []
        for c in seq:
            if unicodedata.category(c) == 'Mn':
                continue
            output.append(c)
        return ''.join(output)


class __Test:
    """"""

    def __init__(self):
        """"""
        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'=== Start "{k}" {{')
                start = time.time()
                v(self)
                print(f'}} End "{k}" - Spend {time.time() - start:f}s===\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_xxx(self):  # noqa
        """"""
        pass


if __name__ == '__main__':
    """"""
    __Test()
