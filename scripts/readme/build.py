#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-10-08 11:31
Author:
    huayang (imhuay@163.com)
Subject:
    build
"""
from __future__ import annotations

import os
# import sys
# import json
# import unittest
import subprocess

# from typing import *
# from pathlib import Path
# from collections import defaultdict

from readme._base import build
from readme.algorithms import AlgorithmsBuilder
from readme.notes import NotesBuilder
from readme.utils import args, ReadmeUtils, readme_tag


class BuildReadme:

    def __init__(self):
        """"""
        self.fp_repo = args.fp_repo
        self._fp_repo_readme = args.fp_repo_readme
        self.algo = AlgorithmsBuilder()
        self.note = NotesBuilder()

    commit_info = 'Auto-Update README'

    def git_push(self):
        os.system('git add -u')
        code, data = subprocess.getstatusoutput(f'git commit -m "{self.commit_info}"')
        if code == 0:
            # os.system('git push')
            data = subprocess.getoutput('git push')
            print(data)
        else:
            print(data)

    def build(self):
        # build
        build(self.algo, self.note)

        # build repo readme
        self._update_homepage()

    def _update_homepage(self):
        with open(self._fp_repo_readme, encoding='utf8') as f:
            txt = f.read()

        txt_index = f'<!-- no toc -->\n{self.algo.toc_append}\n{self.note.toc_append}'
        txt = ReadmeUtils.replace_tag_content(readme_tag.index, txt, txt_index)
        txt = ReadmeUtils.replace_tag_content(readme_tag.recent, txt, self.note.recent_toc_append)
        txt = ReadmeUtils.replace_tag_content(readme_tag.algorithms, txt, self.algo.readme_append)
        txt = ReadmeUtils.replace_tag_content(readme_tag.notes, txt, self.note.readme_append)

        with open(self._fp_repo_readme, 'w', encoding='utf8') as f:
            f.write(txt)


if __name__ == '__main__':
    """"""
    br = BuildReadme()
    br.build()
