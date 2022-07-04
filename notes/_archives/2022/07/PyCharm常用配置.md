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

---

## 常用配置

### 禁止 import 折叠
> Code Folding -> Imports

### 修改 Docstring 风格
> Docstring format -> Google

### 快捷键修改
> Plugins -> Marketplace -> Eclipse Keymap


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