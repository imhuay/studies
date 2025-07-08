#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-03-19 4:57 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import re
import logging
import json

from pathlib import Path

from collections import defaultdict

# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)


class AlgorithmReadme:
    """
    Algorithm README 生成

    TODO:
        - 问题分类、精选问题才会加入

    """
    logger = logging.getLogger('AlgorithmReadme')
    ALGORITHMS = 'algorithms'
    PROBLEMS = 'problems'
    NOTES = 'notes'

    main_dir = os.path.join('..', ALGORITHMS)
    problems_dir = os.path.join(main_dir, PROBLEMS)
    notes_dir = os.path.join(main_dir, NOTES)
    algorithm_readme_path = os.path.join(main_dir, 'README.md')
    all_problems_info: dict
    '''{
        'path/to/牛客_0050_中等_链表中的节点每k个一组翻转.md': info,
        ...
    }'''
    tag2topic = json.load(open(os.path.join(main_dir, 'tag2topic.json'), encoding='utf8'))
    topic2problems: dict
    '''{
        '合集-xxx': [问题路径]
    }'''
    src2problems: dict

    RE_INFO = re.compile(r'<!--(.*?)-->', flags=re.S)
    RE_TAG = re.compile(r'Tag: (.*?)\s')
    RE_SEP = re.compile(r'[,，、]')

    git_add_buf = set()

    AUTO_GENERATED = '<!-- Auto-generated -->'

    def __init__(self):
        """"""
        print('=== AlgorithmReadme Start ===')
        self.load_all_problems()
        self.get_tag2problems()
        self.gen_algorithm_readme()
        self.get_topic_collections()
        print('=== AlgorithmReadme End ===')

    def get_main_content(self, fp):  # noqa
        """"""
        if not os.path.exists(fp):
            return []

        lns = []
        txt = open(fp, encoding='utf8').read()
        for ln in txt.split('\n'):
            lns.append(ln)
            if ln == self.AUTO_GENERATED:
                break

        return lns

    def gen_algorithm_readme(self):
        """"""
        lns = self.get_main_content(self.algorithm_readme_path)

        # def sort_key(x):
        #     if x.startswith('合集'):
        #         return 0, x
        #     else:
        #         return 1, x
        #
        # tmp = sorted(self.topic2problems.keys(), key=sort_key)

        # 合集
        lns.append('')
        cnt = [sum(len(it) for k, it in self.topic2problems.items() if k.startswith("合集"))]
        lns.append(f'## 合集 {cnt}')
        for topic, ps in self.topic2problems.items():
            if topic.startswith('合集'):
                lns.append(f'- [{topic}](./{self.NOTES}/{topic}.md) [{len(ps)}]')

        # 细分类型
        lns.append('')
        lns.append('## 细分类型')
        for topic, ps in self.topic2problems.items():
            if not topic.startswith('合集'):
                lns.append(f'- [{topic}](./{self.NOTES}/{topic}.md) [{len(ps)}]')

        fw = open(self.algorithm_readme_path, 'w', encoding='utf8')
        fw.write('\n'.join(lns))

    def get_topic_collections(self):
        """"""
        for topic, problems in self.topic2problems.items():
            fp = os.path.join(self.notes_dir, f'{topic}.md')
            lns = self.get_main_content(fp)

            if not lns:
                lns.append(f'# {topic}')
                lns.append(f'> [Problems](#problems)')
                lns.append('')
                lns.append(self.AUTO_GENERATED)

            lns.append('')
            lns.append(f'## Problems <!-- omit in toc --> ')
            for p in problems:
                p = Path(p)
                lns.append(f'- [`{p.stem}`]({".." / p.relative_to(self.main_dir)})')

            flag = not os.path.exists(fp)
            fw = open(fp, 'w', encoding='utf8')
            fw.write('\n'.join(lns))
            if flag:
                self.git_add(fp)

    def git_add(self, fp):
        if fp in self.git_add_buf:
            return

        self.git_add_buf.add(fp)
        command_ln = f'git add "{fp}"'
        self.logger.info(command_ln)
        os.system(command_ln)

    def load_all_problems(self):
        """"""
        tmp = dict()
        for prefix, _, files in os.walk(self.problems_dir):
            for fn in files:
                name, ext = os.path.splitext(fn)
                if ext != '.md' or name.startswith('-') or name.startswith('_'):
                    continue

                fp = Path(os.path.join(prefix, fn))
                txt = open(fp, encoding='utf8').read()
                try:
                    info_ret = self.RE_INFO.search(txt)
                    info = json.loads(info_ret.group(1))
                except:
                    raise ValueError(f'parse info error: {fp}')
                fp = self.try_rename(info, fp)
                self.try_add_title(fp, txt)
                tmp[str(fp)] = info

        self.all_problems_info = tmp

    def try_add_title(self, fp, txt):  # noqa
        """"""
        src, no, lv, name = fp.stem.split('_')
        date = '-'.join(str(fp.parent).split('/')[-2:])
        # title = f'## {name}（{src}-{no}, {lv}, {date}）'
        title = f'## {src}_{no}_{name}（{lv}, {date}）'

        flag = True
        lns = txt.split('\n')
        first_ln = lns[0]
        if not first_ln.startswith('##'):
            lns.insert(0, title)
        elif first_ln != title:
            lns[0] = title
        else:
            flag = False

        if flag:
            fw = open(fp, 'w', encoding='utf8')
            fw.write('\n'.join(lns))
            self.git_add(fp)

    def try_rename(self, info, fp):  # noqa
        """"""
        src, no, lv, name = info['来源'], info['编号'], info['难度'], info['标题']
        fn = f'{src}_{no}_{lv}_{name}.md'
        if fn != fp.name:
            self.logger.info(f'rename {fp.name} to {fn}')
            fp = fp.rename(fp.parent / fn)
            self.git_add(fp)
        return fp

    def get_tag2problems(self):
        """"""
        tmp = defaultdict(list)
        for fp, info in self.all_problems_info.items():
            tags = [tag.strip() for tag in info['tags']] + [info['来源']]
            tag2topic = {tag: self.tag2topic[tag.lower()] for tag in tags}
            topics = list(tag2topic.values())
            for topic in topics:
                tmp[topic].append(fp)

        for k, v in tmp.items():
            tmp[k] = sorted(v, key=lambda x: Path(x).name)

        self.topic2problems = dict(sorted(tmp.items()))

    def get_head(self, prefix, fn, info):  # noqa
        """"""
        suffix = '-'.join(prefix.split('/')[-2:])
        src, pid, lv, pn = info['来源'], info['编号'], info['难度'], info['标题']
        head = f'`{src} {pid} {pn} ({lv}, {suffix})`'
        return head

    def get_tag2topic(self):
        notes_dir = self.notes_dir
        file_names = os.listdir(notes_dir)

        tmp = dict()
        for fn in file_names:
            topic, _ = os.path.splitext(fn)
            txt = open(os.path.join(notes_dir, fn), encoding='utf8').read()
            tags = self.RE_SEP.split(self.RE_TAG.search(txt).group(1))
            tmp[topic] = tags

        self.tag2topic = {v.lower(): k for k, vs in tmp.items() for v in vs}


def pipeline():
    """"""
    AlgorithmReadme()


class Test:
    def __init__(self):
        """"""
        doctest.testmod()
        # self.test_AlgorithmReadme()

    def test_AlgorithmReadme(self):  # noqa
        """"""
        AlgorithmReadme()
        # print(json.dumps(ar.tag2topic, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    """"""
    pipeline()
