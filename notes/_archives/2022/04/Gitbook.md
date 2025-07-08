GitBook 使用指南
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [安装](#安装)
- [基本用法](#基本用法)
- [存在问题](#存在问题)
- [参考资料](#参考资料)

---

## 安装

- 安装 node.js（略）；
- **高版本 NodeJs 安装 gitbook 会失败**，使用 `n` 模块管理 node 版本
    ```shell
    $ sudo npm install n -g  # 安装 n 模块
    $ sudo n 10.24.1  # 安装/切换 node 版本到 10.24.1
    $ node -v
    v10.24.1
    ```
- 安装 gitbook
    > [gitbook-cli - npm](https://www.npmjs.com/package/gitbook-cli)
    ```shell
    $ npm install -g gitbook-cli
    $ gitbook -V
    CLI version: 2.3.2
    GitBook version: 3.2.3
    ```

## 基本用法

**初始化文件夹**
```shell
$ gitbook init
```
- 该操作会在目录下新增以下文件（如果存在则跳过）
    - `README.md`
    - `SUMMARY.md`
        - 定义笔记的目录结构
        - 示例
            ```markdown
            # Summary
            - [Introduction](README.md)
            - [part1](part1/README.md)
                - [概述](part1/概述.md)
            - [part2](part2/README.md)
                - [概述](part2/概述.md)
            ```
    - `package-lock.json`

**构建笔记**
```shell
$ gitbook build
```

**启动服务**
```shell
$ gitbook serve
```

## 存在问题
- 对 Markdown 和 HTML 混编的文本展示不好；
- 目前官方已不再维护 gitbook-cli 工具，转而在线工具，详见 www.gitbook.com

## 参考资料
- [Gitbook安装使用教程 - wangyufeng - 博客园](https://www.cnblogs.com/fenggedainifei/p/15500749.html)
- [Gitbook操作指南——搭建个人电子书教程_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1dv411J7B8)