#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-26 11:32
Author:
    HuaYang(imhuay@163.com)
Subject:
    本仓库的 Git Push 脚本，用于处理一些条件场景（纯 Shell 命令不熟）
Usage:
    # 在仓库顶层目录执行
    > python scripts/git_push.py
"""
import os
import sys
import json
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

try:
    def get_repo_top():
        p = Path(__file__).parent
        while all(it.name != '.git' for it in p.iterdir()):
            p = p.parent
        return p


    src_path = get_repo_top() / 'src'
    sys.path.append(str(src_path))
except:  # noqa
    exit(1)
else:
    from huaytools_local.utils.git_utils import GitUtils, GitSubtreeUtils
    from huaytools_local.utils import get_logger, get_caller_name
    from huaytools_local.utils import PrintUtils


class GitHelper:
    """"""
    _logger = get_logger()

    # `src` sub repo
    src_prefix = 'src'
    src_branch = 'sync_src'
    src_repo_url = r'https://github.com/imhuay/sync_src.git'
    src_repo_branch = 'master'

    def __init__(self):
        """"""
        code = self.push_main()
        if code == 0:
            self.push_sub_src()

    def push_main(self):
        """主仓库推送"""
        self._logger.info(PrintUtils.green(f'Start push main repo.'))
        code, data = GitUtils.push()
        if code == 0:
            self._logger.info(PrintUtils.green(f'Push main repo Success. '
                                               f'{{\n{data}\n}}'))
        else:
            self._logger.info(PrintUtils.red(f'Some error when push main repo. '
                                             f'{{\n{data}\n}}'))

        return code

    def push_sub_src(self):
        """子仓库 src 推送"""
        self._logger.info(PrintUtils.green(f'Start push sub repo "{self.src_prefix}".'))
        try:
            code, data = GitSubtreeUtils.push(self.src_repo_url, self.src_repo_branch, self.src_prefix)
            if code != 0:
                self._logger.warning(PrintUtils.red(f'Try `git subtree push --rejoin` failed, '
                                                    f'remove `--rejoin` and retry.'))
                raise RuntimeError
        except RuntimeError:
            code, data = GitSubtreeUtils.push(self.src_repo_url, self.src_repo_branch, self.src_prefix,
                                              assert_not_rejoin=True)

        if code == 0:
            self._logger.info(PrintUtils.green(f'Push sub repo "{self.src_prefix}" Success. '
                                               f'{{\n{data}\n}}'))
        else:
            self._logger.warning(PrintUtils.red(f'Some error when push sub repo "{self.src_prefix}". '
                                                f'{{\n{data}\n}}'))

            PrintUtils.cprint(f'Force push? (Y/n)')
            if (i := input().lower()) != 'y':
                print(i)
                exit(1)
            else:
                code, data = GitSubtreeUtils.force_push(self.src_repo_url, self.src_repo_branch, self.src_prefix, self.src_branch)
                print(code, data)


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
        GitHelper()


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
