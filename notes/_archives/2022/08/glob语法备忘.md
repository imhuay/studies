glob 语法备忘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

<!-- TOC -->
- [通配符](#通配符)
    - [参考](#参考)
- [示例](#示例)
    - [python (`Path.glob()`)](#python-pathglob)
    - [zsh 环境 (mac)](#zsh-环境-mac)
<!-- TOC -->


## 通配符

通配符 | 描述
---------|----------
 `*` | 匹配 0 个或多个任意字符，等价于一般正则中的 `.*`
 `**` | 匹配任意层级的目录，示例 `**/*.txt`
 `?` | 匹配 1 个任意字符，等价于一般正则中的 `.`
 `[abc]` | 匹配给定的字符，与一般正则中含义相同
 `[a-z]` | 匹配给定范围内的字符，与一般正则中含义相同
 `[!abc]` | 匹配任意非给定的字符，等价于一般正则中的 `[^abc]`
 `[!a-z]` | 匹配任意非给定范围内的字符，等价于一般正则中的 `[^a-z]`
 `{a,b}` | 匹配子模式之一，示例 `*.{py,c*}`，等价于 `*.(py\|c*)`

- 有的系统中使用 `!` 需要转义

### 参考
- [glob (programming) - Wikipedia](https://en.wikipedia.org/wiki/Glob_(programming))
- [Glob with Java NIO - Javapapers](https://javapapers.com/java/glob-with-java-nio/)

## 示例

**测试目录**
```shell
-> % tree .
.
├── a1.c
├── a2.py
├── a3.cpp
└── foo
    ├── bar
    │   ├── d1.py
    │   ├── d2.cpp
    │   └── d3.c
    ├── baz
    │   ├── b1.py
    │   ├── b2.c
    │   └── b3.cpp
    ├── c1.py
    ├── c2.cpp
    └── c3.c
```

### python (`Path.glob()`)

- 不支持 `{}` 通配符

```shell
-> % python
Python 3.9.13 | packaged by conda-forge | (main, May 27 2022, 17:00:33) 
[Clang 13.0.1 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from pathlib import Path
>>> r = Path('.').absolute(); r
PosixPath('/Users/huay/tmp/glob_test')

# a*
>>> for p in r.glob('a*'): print(p)
... 
/Users/huay/tmp/glob_test/a1.c
/Users/huay/tmp/glob_test/a3.cpp
/Users/huay/tmp/glob_test/a2.py

# a[13]*
>>> for p in r.glob('a[13]*'): print(p)
... 
/Users/huay/tmp/glob_test/a1.c
/Users/huay/tmp/glob_test/a3.cpp

# a[!13]*
>>> for p in r.glob('a[!13]*'): print(p)
... 
/Users/huay/tmp/glob_test/a2.py

# *.c*
>>> for p in r.glob('*.c*'): print(p)
... 
/Users/huay/tmp/glob_test/a1.c
/Users/huay/tmp/glob_test/a3.cpp

# */*.c*
>>> for p in r.glob('*/*.c*'): print(p)
... 
/Users/huay/tmp/glob_test/foo/c2.cpp
/Users/huay/tmp/glob_test/foo/c3.c

# **/*.cpp
>>> for p in r.glob('**/*.cpp'): print(p)
... 
/Users/huay/tmp/glob_test/a3.cpp
/Users/huay/tmp/glob_test/foo/c2.cpp
/Users/huay/tmp/glob_test/foo/baz/b3.cpp
/Users/huay/tmp/glob_test/foo/bar/d2.cpp

# *.{py, cp*}  Python 不支持
>>> for p in r.glob('*.{py, cp*}'): print(p)
... 

# *.?
>>> for p in r.glob('*.?'): print(p)
... 
/Users/huay/tmp/glob_test/a1.c

# */*.?
>>> for p in r.glob('*/*.?'): print(p)
... 
/Users/huay/tmp/glob_test/foo/c3.c

# */*/*.?
>>> for p in r.glob('*/*/*.?'): print(p)
... 
/Users/huay/tmp/glob_test/foo/baz/b2.c
/Users/huay/tmp/glob_test/foo/bar/d3.c
```

### zsh 环境 (mac)
- 多数结果与 Python 环境相同；
- 使用 `!` 符号，需要转义；
- 支持 `{}` 模式；
```shell
-> % ll a[\!13]*
-rw-r--r--  1 huay  staff     0B  8 26 18:01 a2.py

-> % ll a[^13]*   
-rw-r--r--  1 huay  staff     0B  8 26 18:01 a2.py

-> % ll *.{py,cp*}
-rw-r--r--  1 huay  staff     0B  8 26 18:01 a2.py
-rw-r--r--  1 huay  staff     0B  8 26 18:01 a3.cpp
```