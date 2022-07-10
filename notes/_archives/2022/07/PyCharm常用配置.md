PyCharm 常用配置
===

- [常用配置](#常用配置)
    - [禁止 import 折叠](#禁止-import-折叠)
    - [修改 Docstring 风格](#修改-docstring-风格)
    - [快捷键修改](#快捷键修改)
- [代码模板](#代码模板)
    - [Python](#python)
    - [Python Console](#python-console)
- [常用插件](#常用插件)
    - [主题](#主题)
    - [键位映射](#键位映射)
- [FAQ](#faq)
    - [【Mac】全屏模式下打开新项目默认在新 Tab 而不是新窗口](#mac全屏模式下打开新项目默认在新-tab-而不是新窗口)

---

## 常用配置

### 禁止 import 折叠
> Code Folding -> Imports

### 修改 Docstring 风格
> Docstring format -> Google

### 快捷键修改
- 安装插件：Plugins -> Marketplace -> Eclipse Keymap
- [常用快捷键](./快捷键记录.md#pycharm)


## 代码模板

### Python
> File and Code Templates -> Python Script

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    ${YEAR}-${MONTH}-${DAY} ${TIME}
Author:
    HuaYang(imhuay@163.com)
Subject:
    TODO
"""
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        doctest.testmod()


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
```

### Python Console
> Python Console

```python
%load_ext autoreload
%autoreload 2

import os
import sys

print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])

# import numpy as np

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
```


## 常用插件

### 主题
- [Dracula Theme](https://plugins.jetbrains.com/plugin/12275-dracula-theme)（推荐）
- [One Dark theme](https://plugins.jetbrains.com/plugin/11938-one-dark-theme)


### 键位映射
- [Eclipse Keymap](https://plugins.jetbrains.com/plugin/12559-eclipse-keymap)


## FAQ

### 【Mac】全屏模式下打开新项目默认在新 Tab 而不是新窗口
- **问题描述**：在全屏模式下打开新项目，默认在当前窗口的 Tab 页打开，而不是新窗口；这个问题不是因为 PyCharm 导致的，而是 Mac 的设置；
    <div align="center"><img src="./_assets/pycharm_tag_fix.png" height="" /></div>
- **解决方法**：`系统偏好设置 -> 通用 -> 首选以标签页方式打开文稿` 改为 `永不`；
    <div align="center"><img src="./_assets/pycharm_tag_fix2.png" height="" /></div>