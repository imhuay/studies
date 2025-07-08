#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-28 20:19
Author:
    huayang (imhuay@163.com)
Subject:
    algo
"""
from __future__ import annotations

# import os
# import sys
# import unittest
import os
import re

from typing import ClassVar
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

import yaml

from huaytools.utils import MarkdownUtils
from readme.utils import args, ReadmeUtils
from readme._base import Builder


@dataclass(unsafe_hash=True)
class Tag:
    name: str
    type: str
    is_hot: bool = False
    aliases: list[str] = field(default_factory=list, hash=False)
    notes: list[str] = field(default_factory=list, hash=False)
    _problems: list[Problem] = field(default_factory=list, hash=False)

    def add_problem(self, p: Problem):
        self._problems.append(p)

    @property
    def problems(self):
        return sorted(set(self._problems), key=lambda i: i.sort_key)

    def __post_init__(self):
        self.aliases.insert(0, self.name)
        self.aliases = sorted(set(self.aliases), key=self.aliases.index)

    @property
    def title(self):
        return self.name

    @property
    def count(self):
        return len(self.problems)

    @property
    def toc_line(self):
        return f'- [{self.title} ({self.count})](#{MarkdownUtils.slugify(self.title)})'

    @property
    def toc(self):
        lns = [f'### {self.title}']
        if self.notes:
            lns.append('- **相关笔记** 🔗')
            for n in self.notes:
                _p = Path(n)
                lns.append(f'    - [{_p.stem}](../notes/_archives/{_p})')
            lns.append('')
        lns.append(ReadmeUtils.get_badge('total', self.count, 'blue'))
        for p in self.problems:
            lns.append(p.toc_line)
        return '\n'.join(lns)

    @property
    def sort_key(self):
        return self.count, self.name


@dataclass()
class TagType:
    name: str
    priority: int
    tags: list[Tag] = field(default_factory=list, hash=False)

    @property
    def toc(self):
        lns = []
        for tag in self.sorted_tags:
            lns.append(tag.toc_line)
        return '\n'.join(lns)

    @property
    def sorted_tags(self):
        return sorted(self.tags, key=lambda i: i.sort_key, reverse=True)


class _TagInfo:
    # name2key: dict[str, str] = dict()
    # key2tag: dict[str, Tag] = dict()
    tags: list[Tag] = list()
    alias2tags: dict[str, list[Tag]] = defaultdict(list)
    type2tags: dict[str, TagType] = dict()
    hot_tags: list[Tag] = []

    def __init__(self):
        self._fp_tag_info = args.fp_algorithms_tag_info

        self._load_tag_info()

    def _load_tag_info(self):
        with self._fp_tag_info.open(encoding='utf8') as f:
            _tag_info: list[dict] = yaml.safe_load(f.read())

        for it in _tag_info:
            tag_type: str = it['tag_type']
            priority: int = int(it['priority'])
            self.type2tags[tag_type] = TagType(tag_type, priority)
            tags: dict = it['tags']
            for name, info in tags.items():
                info = info or dict()
                info.setdefault('name', name)
                info.setdefault('type', tag_type)
                tag = Tag(**info)
                self.tags.append(tag)
                self.type2tags[tag_type].tags.append(tag)
                if tag.is_hot:
                    self.hot_tags.append(tag)
                for alias in tag.aliases:
                    self.alias2tags[ReadmeUtils.norm(alias)].append(tag)

    @property
    def hot_tags_sorted(self):
        return sorted(self.hot_tags, key=lambda i: i.sort_key, reverse=True)


tag_info = _TagInfo()


@dataclass(unsafe_hash=True)
class Problem:
    _path: Path

    # property
    _info = None
    _file_name = None
    _title = None
    _last_commit_time = None

    _TAG_BADGE = 'badge'

    def __post_init__(self):
        self.update_file()

    def update_file(self):
        # try update title
        with self.path.open(encoding='utf8') as f:
            txt = f.read()

        lns = txt.split('\n', maxsplit=1)
        if lns[0].startswith('##'):
            lns[0] = self.head
        else:
            lns.insert(0, self.head)

        if not ReadmeUtils.get_tag_content(self._TAG_BADGE, txt):
            lns.insert(1, ReadmeUtils.get_tag_begin(self._TAG_BADGE))
            lns.insert(2, ReadmeUtils.get_tag_end(self._TAG_BADGE))

        txt = ReadmeUtils.replace_tag_content(self._TAG_BADGE,
                                              '\n'.join(lns),
                                              self.badge_content)
        with self.path.open('w', encoding='utf8') as f:
            f.write(txt)

    @property
    def badge_content(self):
        lns = [ReadmeUtils.get_last_modify_badge_url(self.path)]
        used = set()
        lns.append(ReadmeUtils.get_badge('', message=self.level, color='yellow',
                                         url=f'../../../README.md#{MarkdownUtils.slugify(self.level)}'))
        lns.append(ReadmeUtils.get_badge('', message=self.source, color='green',
                                         url=f'../../../README.md#{MarkdownUtils.slugify(self.source)}'))
        for t in self.tags:
            for tag in tag_info.alias2tags[ReadmeUtils.norm(t)]:
                if tag not in used:
                    used.add(tag)
                    lns.append(ReadmeUtils.get_badge('', message=tag.name, color='blue',
                                                     url=f'../../../README.md#{MarkdownUtils.slugify(tag.title)}'))
        return '\n'.join(lns)

    # @property
    # def message_tags(self):
    #     return ', '.join([tag_info.alias2tag[ReadmeUtils.norm(tag)].name for tag in self.tags])

    @property
    def path(self):
        if self.file_name != self._path.name:
            new_path = self._path.parent / self.file_name
            ReadmeUtils.git_mv(self._path, new_path)
            self._path = new_path
        return self._path

    @property
    def title(self):
        # if self._title is None:
        #     self._title = '{name} ({src}, {level})'.format(name=self.name,
        #                                                    src=self.source,
        #                                                    level=self.level)
        # return self._title
        return self.name

    @property
    def sort_key(self):
        return self.source, self.number

    @property
    def head(self):
        return f'## {self.title}'

    @property
    def toc_line(self):
        return f'- [`{self.path.stem}`]({self.path.relative_to(args.fp_algorithms)})'

    @property
    def last_commit_time(self):
        if self._last_commit_time is None:
            ReadmeUtils.get_last_commit_date(self.path)
        return self._last_commit_time

    @property
    def file_name(self):
        if self._file_name is None:
            self._file_name = '{src}_{no}_{level}_{name}.md'.format(src=self.source,
                                                                    no=self.number,
                                                                    level=self.level,
                                                                    name=re.sub(r'\s+', '', self.name))
        return self._file_name

    @property
    def info(self):
        if self._info is None:
            with self._path.open(encoding='utf8') as f:
                txt = f.read()
            try:
                info_str = ReadmeUtils.get_annotation_info(txt)
                self._info = yaml.safe_load(info_str.strip())
            except:  # noqa
                raise ValueError(self._path)
        return self._info

    _F_TAGS: ClassVar[str] = 'tags'
    _F_SOURCE: ClassVar[str] = 'source'
    _F_NUMBER: ClassVar[str] = 'number'
    _F_LEVEL: ClassVar[str] = 'level'
    _F_NAME: ClassVar[str] = 'name'
    _F_COMPANIES: ClassVar[str] = 'companies'

    @property
    def tags(self) -> list[str]:
        return self.info[Problem._F_TAGS]

    @property
    def source(self) -> str:
        return self.info[Problem._F_SOURCE]

    @property
    def number(self) -> str:
        return self.info[Problem._F_NUMBER]

    @property
    def level(self) -> str:
        return self.info[Problem._F_LEVEL]

    @property
    def name(self) -> str:
        return self.info[Problem._F_NAME]

    @property
    def companies(self) -> list[str]:
        return self.info[Problem._F_COMPANIES]


class AlgorithmsBuilder(Builder):
    """"""
    problems: list[Problem]

    def __init__(self):
        self._fp_algo = args.fp_algorithms
        self._fp_algo_readme = args.fp_algorithms_readme
        self._fp_problems = args.fp_algorithms_problems

        self.alias2tags = tag_info.alias2tags
        self.type2tags = tag_info.type2tags
        self.title = args.algorithms_readme_title

        self._load_problems()

    def _load_problems(self):
        self.problems = []
        for dp, _, fns in os.walk(self._fp_problems):
            for fn in fns:
                fp = Path(dp) / fn  # each problem.md
                if fp.suffix != '.md':
                    continue
                self.problems.append(Problem(fp))

        for p in self.problems:
            [tag.add_problem(p) for tag in self.alias2tags[ReadmeUtils.norm(p.source)]]
            [tag.add_problem(p) for tag in self.alias2tags[ReadmeUtils.norm(p.level)]]
            for name in p.tags:
                [tag.add_problem(p) for tag in self.alias2tags[ReadmeUtils.norm(name)]]

    @property
    def hot_toc(self):
        lns = []
        for tag in tag_info.hot_tags_sorted:
            lns.append(tag.toc_line)
        return '\n'.join(lns)

    @property
    def problems_toc(self):
        lns = []
        for tag_type in sorted(self.type2tags.values(), key=lambda i: i.priority):
            for tag in tag_type.sorted_tags:
                lns.append(tag.toc)
                lns.append('')
        return '\n'.join(lns)

    @property
    def readme_append(self):
        with self._fp_algo_readme.open(encoding='utf8') as f:
            txt = f.read()
        section = ReadmeUtils.get_tag_content('toc', txt)
        return section.replace('](', f']({self._fp_algo_readme.relative_to(args.fp_repo)}')

    @property
    def toc_append(self):
        return f'- [{self.title}](#{MarkdownUtils.slugify(self.title)})'

    @property
    def head(self):
        return f'## {self.title}'

    def build(self):
        with self._fp_algo_readme.open(encoding='utf8') as f:
            txt = f.read()

        # title
        txt = ReadmeUtils.replace_tag_content('head', txt, self.head)

        # hot
        txt = ReadmeUtils.replace_tag_content('hot', txt, self.hot_toc)

        # tags toc
        for tag_type, info in self.type2tags.items():
            txt = ReadmeUtils.replace_tag_content(tag_type, txt, info.toc)

        # problems toc
        txt = ReadmeUtils.replace_tag_content('problems', txt, self.problems_toc)

        with self._fp_algo_readme.open('w', encoding='utf8') as f:
            f.write(txt)


if __name__ == '__main__':
    """"""
    algo = AlgorithmsBuilder()
    algo.build()
