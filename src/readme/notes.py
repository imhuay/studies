#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-10-05 13:15
Author:
    huayang (imhuay@163.com)
Subject:
    notes
"""
from __future__ import annotations

import os
# import os
# import sys
# import json
# import unittest
# import subprocess
import re

import yaml

from typing import ClassVar
from pathlib import Path
from dataclasses import dataclass

from readme._base import Builder
from readme.utils import args, ReadmeUtils, TEMP_main_readme_notes_recent_toc


# TMP_subject_toc = '''### {title}
#
# {toc}
# '''


@dataclass(unsafe_hash=True)
class SubjectId:
    id: str
    name: str


class RE:
    # note_info = re.compile(r'<!--info(.*?)-->', flags=re.DOTALL)
    note_name = re.compile(r'(\d{3})-(.*?).md')
    note_toc = re.compile(r'<!-- TOC -->(.*?)<!-- TOC -->', flags=re.DOTALL)
    note_content = re.compile(r'<!-- CONTENT -->(.*?)<!-- CONTENT -->', flags=re.DOTALL)


# def _load_note_info(fp, txt):
#     m = RE.note_info.search(txt)
#     if not m:
#         raise ValueError(fp)
#     return yaml.safe_load(m.group(1).strip())


@dataclass
class SubjectInfo:
    path: Path
    # subject_ids: ClassVar[dict[str, SubjectId]]

    _prefix = None
    _name = None
    _txt = None
    _toc = None
    _info = None

    @property
    def head(self):
        h_lv = '###' if self.name != 'WIKI' else '##'
        return f'{h_lv} [{self.name}]({self.path.name})'

    @property
    def prefix(self):
        if self._prefix is None:
            self._prefix = self.path.stem.split('-')[0]
        return self._prefix

    @property
    def name(self):
        if self._name is None:
            self._name = self.path.stem.split('-')[1]
        return self._name

    @property
    def subject_id(self) -> str:
        return self.prefix[0]

    @property
    def subject_number(self) -> str:
        return self.prefix[1:]

    @property
    def txt(self):
        if self._txt is None:
            with self.path.open(encoding='utf8') as f:
                self._txt = f.read().strip()
        return self._txt

    @property
    def toc(self) -> str:
        if self._toc is None:
            m = RE.note_toc.search(self.txt)
            if not m:
                raise ValueError(self.path)
            toc = m.group(1).strip()
            toc = toc.replace('(#', f'({self.path.name}#')
            # toc = f'{self.head}\n{toc}'
            self._toc = toc
        return self._toc

    @property
    def info(self) -> dict:
        if self._info is None:
            try:
                _info = ReadmeUtils.get_annotation_info(self.txt)
            except:  # noqa
                raise ValueError(self.path)
            self._info = yaml.safe_load(_info)
        return self._info

    @property
    def toc_id(self):
        return self.info['toc_id']


@dataclass
class NoteInfo:
    top: bool = False
    hidden: bool = False


@dataclass
class Note:
    path: Path
    _info: NoteInfo = None
    _title: str = None
    _first_commit_date: str = None
    _last_commit_date: str = None
    sort_by_first_commit: ClassVar[bool] = True

    def __post_init__(self):
        self.update_note_last_modify()

    def update_note_last_modify(self):
        with self.path.open(encoding='utf8') as f:
            new_txt = ReadmeUtils.replace_tag_content('badge', f.read(),
                                                      ReadmeUtils.get_last_modify_badge_url(self.path))
        with self.path.open('w', encoding='utf8') as f:
            f.write(new_txt)

    @property
    def title(self):
        if self._title is None:
            with self.path.open(encoding='utf8') as f:
                for ln in f:
                    self._title = ln.strip()
                    break

            if not self._title:
                self._title = f'Untitled-{self.path_relative_to_repo}'
        return self._title

    @property
    def info(self) -> NoteInfo:
        if self._info is None:
            with self.path.open(encoding='utf8') as f:
                try:
                    _info_str = ReadmeUtils.get_annotation_info(f.read())
                except:  # noqa
                    raise ValueError(self.path)
                _info: dict
                if _info_str:
                    _info = yaml.safe_load(_info_str)
                else:
                    _info = dict()
            self._info = NoteInfo(**_info)
        return self._info

    @property
    def first_commit_date(self) -> str:
        if self._first_commit_date is None:
            self._first_commit_date = ReadmeUtils.get_first_commit_date(self.path)
        return self._first_commit_date

    @property
    def last_commit_date(self) -> str:
        if self._last_commit_date is None:
            self._last_commit_date = ReadmeUtils.get_last_commit_date(self.path)
        return self._last_commit_date

    @property
    def date(self):
        return self._commit_datetime_for_sort[:10]

    @property
    def is_top(self):
        return self.info.top

    @property
    def is_hidden(self):
        return self.info.hidden

    @property
    def path_relative_to_repo(self):
        return self.path.relative_to(args.fp_repo)

    @property
    def toc_line_relative_to_repo(self):
        """"""
        if self.is_top:
            return f'- [`{self.date}` {self.title} 📌]({self.path_relative_to_repo})'
        else:
            return f'- [`{self.date}` {self.title}]({self.path_relative_to_repo})'

    def get_toc_line_relative_to(self, parent_path: Path):
        if self.is_top:
            return f'- [`{self.date}` {self.title} 📌]({self.path.relative_to(parent_path)})'
        else:
            return f'- [`{self.date}` {self.title}]({self.path.relative_to(parent_path)})'

    @property
    def sort_key(self):
        # if self.title is None:
        #     raise ValueError(self.path)
        # return self.last_commit_date, self.title
        return self._commit_datetime_for_sort, self.title

    @property
    def _commit_datetime_for_sort(self):
        return self.first_commit_date if self.sort_by_first_commit else self.last_commit_date


class NotesBuilder(Builder):

    def __init__(self):
        """"""
        self._fp_notes = args.fp_notes
        self._fp_notes_archives = args.fp_notes_archives
        self._fp_notes_readme = args.fp_notes_readme
        self._fp_notes_readme_temp = args.fp_notes_readme_temp
        self._top_limit = args.notes_top_limit
        # self._recent_limit = args.notes_recent_limit

        self._load_note_indexes()
        self._load_all_notes()

    subjects: list[SubjectInfo]
    fp2date: dict[Path, str]
    notes: list[Note] = []
    _notes_top: list[Note] = []
    _notes_recent: list[Note] = []

    @property
    def recent_limit(self):
        return

    @property
    def notes_top(self):
        return self._notes_top[:self._top_limit]

    @property
    def notes_recent(self):
        recent_limit = len(self.toc_append.split('\n'))
        return self._notes_recent[:recent_limit - len(self.notes_top)]

    def _load_all_notes(self):
        for dp, _, fns in os.walk(self._fp_notes_archives):
            for fn in fns:
                fp = Path(dp) / fn
                if fp.suffix != '.md':
                    continue
                note_i = Note(fp)
                self.notes.append(note_i)
                if not note_i.is_hidden:
                    if note_i.is_top:
                        self._notes_top.append(note_i)
                    else:
                        self._notes_recent.append(note_i)

        self._notes_top.sort(key=lambda x: x.sort_key, reverse=True)
        self._notes_recent.sort(key=lambda x: x.sort_key, reverse=True)

    def _load_note_indexes(self):
        self.subjects = []
        for path in self._fp_notes.iterdir():
            if not RE.note_name.match(path.name):
                continue
            _subject = SubjectInfo(path)
            self.subjects.append(_subject)

    def build(self):
        with self._fp_notes_readme_temp.open(encoding='utf8') as f:
            txt = f.read()

        txt = ReadmeUtils.replace_tag_content('recent', txt, self.recent_toc)

        contents = {s.toc_id: s.toc for s in self.subjects}
        txt = txt.format(**contents)

        with self._fp_notes_readme.open('w', encoding='utf8') as f:
            f.write(txt)

    @property
    def toc_append(self):
        with self._fp_notes_readme.open(encoding='utf8') as f:
            return RE.note_toc.search(f.read()).group(1).strip()

    @property
    def recent_toc(self):
        return TEMP_main_readme_notes_recent_toc.format(
            toc_top='\n'.join([n.get_toc_line_relative_to(self._fp_notes) for n in self.notes_top]),
            toc_recent='\n'.join([n.get_toc_line_relative_to(self._fp_notes) for n in self.notes_recent])
        )

    @property
    def recent_toc_append(self):
        return TEMP_main_readme_notes_recent_toc.format(
            toc_top='\n'.join([n.toc_line_relative_to_repo for n in self.notes_top]),
            toc_recent='\n'.join([n.toc_line_relative_to_repo for n in self.notes_recent])
        )

    @property
    def readme_append(self):
        with self._fp_notes_readme.open(encoding='utf8') as f:
            # content = RE.note_content.search(f.read()).group(1).strip()
            # return content.replace('](', f']({self._fp_notes.name}/')
            txt = f.read()
        txt = ReadmeUtils.get_tag_content('notes', txt)
        return txt.replace('](', f']({self._fp_notes.name}/')


if __name__ == '__main__':
    """"""
    note = NotesBuilder()
    note.build()
