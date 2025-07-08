#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-10-03 23:53
Author:
    huayang (imhuay@163.com)
Subject:
    utils
"""
from __future__ import annotations

import os
import re
# import sys
# import json
# import unittest
import subprocess
from dataclasses import dataclass, fields
from datetime import datetime, timedelta, timezone
# from typing import *
# from collections import defaultdict
from pathlib import Path

from markdown.extensions import toc

from huaytools.utils import get_logger

logger = get_logger()


class MarkdownUtils:

    @staticmethod
    def slugify(head):
        return toc.slugify_unicode(head, '-')  # noqa


class ReadmeUtils:
    BJS = timezone(
        timedelta(hours=8),
        name='Asia/Beijing',
    )

    @staticmethod
    def norm(txt: str):
        return txt.lower()

    GIT_ADD_TEMP = 'git add "{fp}"'

    @staticmethod
    def git_add(fp: Path):
        """不再使用，通过 git add -u 代替"""
        command = ReadmeUtils.GIT_ADD_TEMP.format(fp=fp.resolve())
        code = os.system(command)
        ReadmeUtils._log_command(code, command)

    GIT_MV_TEMP = 'git mv "{old_fp}" "{new_fp}"'

    @staticmethod
    def git_mv(old_fp: Path, new_fp: Path):
        ReadmeUtils.git_add(old_fp)
        command = ReadmeUtils.GIT_MV_TEMP.format(old_fp=old_fp.resolve(), new_fp=new_fp.resolve())
        code = os.system(command)
        ReadmeUtils._log_command(code, command)

    @staticmethod
    def _log_command(code, command):
        if code == 0:
            logger.info(command)
        else:
            logger.error(command)

    # @staticmethod
    # def _get_file_commit_date(fp, first_commit=True, return_datetime=False) -> str | datetime:
    #     tail_or_head = 'tail' if first_commit else 'head'
    #     code, date_str = subprocess.getstatusoutput(
    #         f'git log --follow --format=%ad --date=iso-strict "{fp}" | {tail_or_head} -1')
    #     if code != 0:
    #         raise ValueError(f'{ReadmeUtils._get_file_commit_date.__name__}: {fp}')
    #     if return_datetime:
    #         return datetime.fromisoformat(date_str)
    #     return date_str

    # @staticmethod
    # def get_file_first_commit_date(fp, return_datetime=False) -> str | datetime:
    #     return ReadmeUtils._get_file_commit_date(fp, first_commit=True, return_datetime=return_datetime)

    # TEMP_GIT_LOG_FOLLOW = r'git log --invert-grep --grep="Auto\|AUTO\|auto" --format=%ad --date=iso-strict --follow "{fp}"'  # noqa
    TEMP_GIT_LOG_FOLLOW = r'git log --author=imhuay --invert-grep --grep="Auto\|AUTO"' \
                          r' --format=%ad --date=iso-strict --follow "{fp}"'

    @staticmethod
    def get_first_commit_date(fp, fmt='%Y-%m-%d %H:%M:%S') -> str:
        _, date_str = subprocess.getstatusoutput(f'{ReadmeUtils.TEMP_GIT_LOG_FOLLOW.format(fp=fp)} | tail -1')
        return ReadmeUtils.get_date_str(date_str, fmt)

    @staticmethod
    def get_last_commit_date(fp, fmt='%Y-%m-%d %H:%M:%S') -> str:
        _, date_str = subprocess.getstatusoutput(f'{ReadmeUtils.TEMP_GIT_LOG_FOLLOW.format(fp=fp)} | head -1')
        return ReadmeUtils.get_date_str(date_str, fmt)

    @staticmethod
    def get_date_str(iso_date_str: str, fmt):
        if not iso_date_str:
            dt = datetime.now(ReadmeUtils.BJS)
        else:
            dt = datetime.fromisoformat(iso_date_str)
            dt.astimezone(ReadmeUtils.BJS)
        return dt.strftime(fmt)

    # @staticmethod
    # def get_file_last_commit_date(fp, return_datetime=False) -> str | datetime:
    #     return ReadmeUtils._get_file_commit_date(fp, first_commit=False, return_datetime=return_datetime)

    # RE_WAKATIME = re.compile(r'<!--START_SECTION:waka-->[\s\S]+<!--END_SECTION:waka-->')

    # @staticmethod
    # def extract_wakatime(txt) -> str:
    #     return ReadmeUtils.RE_WAKATIME.search(txt).group()

    SECTION_START = '<!--START_SECTION:{tag}-->'
    SECTION_END = '<!--END_SECTION:{tag}-->'
    SECTION_ANNOTATION = r'<!--{tag}\n(.*?)\n-->'
    TEMP_LAST_MODIFY_BADGE = '![last modify](https://img.shields.io/static/v1?label=last%20modify&message={datetime}&color=yellowgreen&style=flat-square)'  # noqa
    TEMP_BADGE_URL = 'https://img.shields.io/static/v1?{}'

    @staticmethod
    def get_tag_begin(tag):
        return ReadmeUtils.SECTION_START.format(tag=tag)

    @staticmethod
    def get_tag_end(tag):
        return ReadmeUtils.SECTION_END.format(tag=tag)

    @staticmethod
    def replace_tag_content(tag, txt, content) -> str:
        """"""
        re_pattern = ReadmeUtils._get_section_re_pattern(tag)
        repl = f'{ReadmeUtils.get_tag_begin(tag)}\n\n{content}\n\n{ReadmeUtils.get_tag_end(tag)}'
        return re_pattern.sub(repl, txt, count=1)

    @staticmethod
    def get_last_modify_badge_url(fp):
        return ReadmeUtils.get_badge(label='last modify',
                                     message=ReadmeUtils.get_last_commit_date(fp),
                                     color='yellowgreen',
                                     style='flat-square')

    @staticmethod
    def get_badge(label, message, color, style='flat-square', url=None, **options):
        from urllib.parse import quote
        parameters = {
            'label': quote(str(label)),
            'message': quote(str(message)),
            'color': color,
            'style': style,
        }
        parameters.update(options)
        # parameters = {k: quote(str(v)) for k, v in parameters.items()}
        badge_url = ReadmeUtils.TEMP_BADGE_URL.format('&'.join([f'{k}={v}' for k, v in parameters.items()]))
        if url is None:
            return f'![{label}]({badge_url})'
        else:
            return f'[![{label}]({badge_url})]({url})'

    @staticmethod
    def get_tag_content(tag, txt) -> str | None:
        """
        <!--START_SECTION:{tag}-->
        <content>
        <!--END_SECTION:{tag}-->
        """
        re_pattern = ReadmeUtils._get_section_re_pattern(tag)
        m = re_pattern.search(txt)
        if not m:
            return None
        return m.group(1).strip()

    @staticmethod
    def _get_section_re_pattern(tag):
        return re.compile(fr'{ReadmeUtils.get_tag_begin(tag)}(.*?){ReadmeUtils.get_tag_end(tag)}',
                          flags=re.DOTALL)

    @staticmethod
    def get_annotation(tag, txt) -> str | None:
        """
        <!--<tag>
        <info>
        -->
        """
        re_pattern = re.compile(ReadmeUtils.SECTION_ANNOTATION.format(tag=tag), flags=re.DOTALL)
        m = re_pattern.search(txt)
        if m:
            return m.group(1).strip()
        return None

    @staticmethod
    def get_annotation_info(txt) -> str | None:
        """"""
        return ReadmeUtils.get_annotation('info', txt)


@dataclass
class ReadmeTag:
    index: str = None
    recent: str = None
    algorithms: str = None
    notes: str = None
    waka: str = None

    def __post_init__(self):
        for f in fields(self):
            setattr(self, f.name, f.name)


readme_tag = ReadmeTag()


class args:  # noqa
    """"""
    _fp_cur_file = Path(__file__)
    # repo
    fp_repo = Path(_fp_cur_file.parent / '../..').resolve()
    fp_repo_readme = fp_repo / 'README.md'

    # algorithms
    fp_algorithms = Path(fp_repo / 'algorithms')
    fp_algorithms_readme = fp_algorithms / 'README.md'
    fp_algorithms_problems = fp_algorithms / 'problems'
    fp_algorithms_tag_info = fp_algorithms / 'tag_info.yml'
    algorithms_readme_title = 'Algorithm Codings'

    # notes
    fp_notes = Path(fp_repo / 'notes')
    fp_notes_archives = fp_notes / '_archives'
    fp_notes_readme = fp_notes / 'README.md'
    fp_notes_readme_temp = fp_notes / 'README_template.md'
    notes_top_limit = 5


TEMP_main_readme_notes_recent_toc = '''{toc_top}
{toc_recent}
'''
TEMP_main_readme_algorithms_concat = '''## {title}

{toc}
'''

TEMP_algorithm_toc_td_category = '<td width="1000" valign="top">\n\n{sub_toc}\n\n</td>'
TEMP_algorithm_toc_table = '''<table>  <!-- invalid: frame="void", style="width: 100%; border: none; background: none" -->
<tr>
<td colspan="2" valign="top" width="1000">

{toc_hot}

</td>
<td colspan="2" rowspan="3" valign="top" width="1000">

{toc_subject}

</td>
</tr>
<tr></tr>
<tr>
<td colspan="2" valign="top">

{toc_level}

</td>
</tr>
<tr></tr>
<tr>  <!-- loop TMP_TOC_TD_CATEGORY -->

{toc_category}

</tr>
</table>'''
TEMP_algorithm_readme = '''# {title}

{toc}

---

{sub_toc}'''
