Mac 环境配置
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [必备软件](#必备软件)
    - [Homebrew (brew)](#homebrew-brew)
- [常用工具](#常用工具)

## 必备软件

### Homebrew (brew)
> [Homebrew - 软件包管理工具](https://brew.sh/)

安装后需要手动添加环境变量（注意安装完成后的提示）
```shell
$ echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/huay/.zprofile
$ eval "$(/opt/homebrew/bin/brew shellenv)"
```

## 常用工具

```shell
$ brew install cmake
$ brew install pkgconfig
```
