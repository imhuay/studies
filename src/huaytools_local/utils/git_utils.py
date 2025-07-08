#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-26 11:36
Author:
    HuaYang(imhuay@163.com)
Subject:
    Git Utils
"""
import os
import sys
import json
import doctest
import subprocess

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

from huaytools_local.utils._common import get_logger

_logger = get_logger()


class GitUtils:
    """"""
    command_temp: ClassVar[str] = '{base} {options}'  # 命令模板
    OP_TRUE: ClassVar[str] = ''  # bool 型选项的值

    @staticmethod
    def run(base: str, *, options: dict = None):
        """"""
        options = options or {}

        tmp_ops = []
        for key, value in options.items():
            op = f'-{key}' if len(key) == 1 else f'--{key}'
            if value != GitUtils.OP_TRUE:
                op += f' {value}'
            tmp_ops.append(op)
        ops = ' '.join(tmp_ops)
        command = GitUtils.command_temp.format(base=base, options=ops)
        return subprocess.getstatusoutput(command)
        # return os.system(command)

    @staticmethod
    def push(*, force=False, option_dict: Dict[str, str] = None, **options: str):
        """"""
        options.update(option_dict or {})
        GitUtils.update_options(options, 'force', force)
        return GitUtils.run('git push', options=options)

    @staticmethod
    def pull(*, option_dict: Dict[str, str] = None, **options: str):
        """"""
        options.update(option_dict or {})
        return GitUtils.run('git pull', options=options)

    @staticmethod
    def update_options(options: Dict[str, str], key: str, value: Union[str, bool]):
        """"""
        if isinstance(value, bool):
            if value is True:
                options[key] = GitUtils.OP_TRUE
            else:
                options.pop(key, None)
        else:
            options[key] = value

    @staticmethod
    def get_status():
        """"""
        return subprocess.getoutput('git status')

    # @staticmethod
    # def current_no_commit() -> bool:
    #     status = GitUtils.get_status()
    #     return False


class GitSubtreeUtils:
    """"""

    @staticmethod
    def _run(run_type: str, repo_url_or_name: str, repo_branch: str, prefix: str,
             *, option_dict: Dict[str, str] = None, **options: str):
        base = f'git subtree {run_type} {repo_url_or_name} {repo_branch}'
        options.update(option_dict or {})
        GitUtils.update_options(options, 'prefix', prefix)
        return GitUtils.run(base, options=options)

    @staticmethod
    def add(repo_url_or_name: str, repo_branch: str, prefix: str,
            *, squash: bool = True, assert_not_squash: bool = False, option_dict: Dict[str, str] = None,
            **options: str):
        """"""
        if not assert_not_squash:
            GitSubtreeUtils._check_squash(squash)
        else:
            squash = False
        GitUtils.update_options(options, 'squash', squash)
        return GitSubtreeUtils._run('add', repo_url_or_name, repo_branch, prefix,
                                    option_dict=option_dict, **options)

    @staticmethod
    def pull(repo_url_or_name: str, repo_branch: str, prefix: str,
             *, squash: bool = True, assert_not_squash: bool = False, option_dict: Dict[str, str] = None,
             **options: str):
        """"""
        if not assert_not_squash:
            GitSubtreeUtils._check_squash(squash)
        else:
            squash = False
        GitUtils.update_options(options, 'squash', squash)
        return GitSubtreeUtils._run('pull', repo_url_or_name, repo_branch, prefix,
                                    option_dict=option_dict, **options)

    @staticmethod
    def push(repo_url_or_name: str, repo_branch: str, prefix: str,
             *, rejoin: bool = True, assert_not_rejoin: bool = False, squash: bool = None,
             option_dict: Dict[str, str] = None, **options: str):
        """"""
        squash = squash or rejoin
        if assert_not_rejoin:
            rejoin = squash = False
        GitSubtreeUtils._check_rejoin_and_squash(rejoin, assert_not_rejoin, squash)

        GitUtils.update_options(options, 'rejoin', rejoin)
        GitUtils.update_options(options, 'squash', squash)
        return GitSubtreeUtils._run('push', repo_url_or_name, repo_branch, prefix,
                                    option_dict=option_dict, **options)

    @staticmethod
    def force_push(repo_url_or_name: str, repo_branch: str, prefix: str, local_branch: str,
                   *, rejoin: bool = True, assert_not_rejoin: bool = False, squash: bool = None):
        """"""
        code, data = GitSubtreeUtils.split(prefix, local_branch,
                                           rejoin=rejoin, assert_not_rejoin=assert_not_rejoin, squash=squash)
        if code == 0:
            command = f'git push --force {repo_url_or_name} {data}:{repo_branch}'
            return GitUtils.run(command)
        else:
            _logger.warning(data)

    @staticmethod
    def split(prefix: str, branch: str,
              *, rejoin: bool = True, assert_not_rejoin: bool = False, squash: bool = None,
              option_dict: Dict[str, str] = None, **options: str):
        """"""
        base = 'git subtree split'

        squash = squash or rejoin
        if assert_not_rejoin:
            rejoin = squash = False
        GitSubtreeUtils._check_rejoin_and_squash(rejoin, assert_not_rejoin, squash)

        options.update(option_dict or {})
        GitUtils.update_options(options, 'prefix', prefix)
        GitUtils.update_options(options, 'branch', branch)
        GitUtils.update_options(options, 'rejoin', rejoin)
        GitUtils.update_options(options, 'squash', squash)
        return GitUtils.run(base, options=options)

    @staticmethod
    def _check_rejoin_and_squash(rejoin: bool, assert_not_rejoin: bool, squash: bool):
        if assert_not_rejoin and squash:
            raise ValueError('`squash` is invalid when `rejoin` is not enabled.')
        if not assert_not_rejoin and not rejoin:
            raise ValueError(f'Suggesting add `--rejoin` when `git subtree split/push`, '
                             f'if assert not rejoin, set `assert_not_rejoin=True`.')

    @staticmethod
    def _check_squash(squash: bool):
        if not squash:
            raise ValueError(f'Suggesting add `--squash` when `git subtree add`, '
                             f'if assert not squashing, set `assert_not_squash=True`.')


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
        print(subprocess.getstatusoutput('git subtree split --branch sync_src1 --rejoin --prefix=src'))


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
