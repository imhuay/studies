Markdown 语法备忘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-01-13%2021%3A23%3A34&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

<!-- TOC -->
- [基本语法](#基本语法)
    - [表格](#表格)
    - [参考链接 (Reference-style Links)](#参考链接-reference-style-links)
- [扩展语法](#扩展语法)
    - [表格 (Table)](#表格-table)
    - [注脚 (Footnotes)](#注脚-footnotes)
    - [下标 (Subscript)](#下标-subscript)
    - [上标 (Superscript)](#上标-superscript)
    - [任务列表 (Task Lists)](#任务列表-task-lists)
    - [高亮 (Highlight)](#高亮-highlight)
- [其他编辑技巧](#其他编辑技巧)
    - [元素居中](#元素居中)
    - [目录块 (类似 `tree` 命令生成)](#目录块-类似-tree-命令生成)
    - [换行](#换行)
    - [图片 (HTML)](#图片-html)
    - [隐藏块](#隐藏块)
    - [表格 (HTMl)](#表格-html)
- [Latex](#latex)
    - [引用](#引用)
    - [对齐](#对齐)
- [VSCode 插件](#vscode-插件)
    - [自动更新目录插件](#自动更新目录插件)
<!-- TOC -->


## 基本语法
> [Basic Syntax | Markdown Guide](https://www.markdownguide.org/basic-syntax)

### 表格

### 参考链接 (Reference-style Links)

```markdown
[hobbit-hole][1]

<!-- 以下等价 -->

[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle "Hobbit lifestyles"
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle 'Hobbit lifestyles'
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle (Hobbit lifestyles)
[1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> "Hobbit lifestyles"
[1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> 'Hobbit lifestyles'
[1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> (Hobbit lifestyles)
```

[hobbit-hole][1]

> 在预览界面, 引用内容会被隐藏

[1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> "Hobbit lifestyles"

## 扩展语法
> [Extended Syntax | Markdown Guide](https://www.markdownguide.org/extended-syntax)
>> 并非所有 Markdown 程序都支持扩展语法

### 表格 (Table)

```markdown
| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
```

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

### 注脚 (Footnotes)

```markdown
Here's a simple footnote[^1], and here's a longer one[^bignote].

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.
```

Here's a simple footnote[^1], and here's a longer one[^bignote].

> 在预览界面, 注脚内容会被转移到文档末尾; 如果注脚内容没有被任何地方引用, 则会被隐藏;

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.

[^no_ref]: Content that is not referenced will be hidden.

### 下标 (Subscript)

```markdown
H~2~O
```

**等价 HTML 语法**

```html
H<sub>2</sub>O
```

H<sub>2</sub>O

### 上标 (Superscript)
> GitHub 暂不支持
```markdown
X^2^
```

**等价 HTML 语法**

```html
X<sup>2</sup>
```

X<sup>2</sup>


### 任务列表 (Task Lists)

```markdown
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
```

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media

### 高亮 (Highlight)

```markdown
I need to highlight these ==very important words==.
```

**等价 HTML 语法**

```html
I need to highlight these <mark>very important words</mark>.
```

I need to highlight these <mark>very important words</mark>.


## 其他编辑技巧

### 元素居中
```html
<!-- 通用 -->
<div align="center">
    content
</div>

<!-- GitHub 上不生效 -->
<div style="text-align: center;">
    content
</div>
```

<div align="center">
    content
</div>


### 目录块 (类似 `tree` 命令生成)
```txt
project
├── src/
│   ├── assets/                    // 静态资源目录
│   ├── common/                    // 通用类库目录
│   ├── components/                // 公共组件目录
│   ├── store/                     // 状态管理目录
│   ├── utils/                     // 工具函数目录
│   ├── App.vue
│   └── main.ts
├── tests/                         // 单元测试目录
├── index.html
└── package.json
```

### 换行
- 法1）在行末手动插入 `<br/>`；
- 法2）在行末添加两个空格；

### 图片 (HTML)

- 不带链接
    ```html
    <img src="..." height="300" />
    ```
- 带链接
    ```html
    <a href=""><img src="..." height="300" /></a>
    ```
    - `height`用于控制图片的大小，一般不使用，图片会等比例缩放；
- 居中
    ```html
    <div align="center"><img src="..." height="300" /></div>
    ``` 

### 隐藏块
```html
<details><summary><b>点击展开</b></summary> 

// 代码块，注意上下都要保留空行

</details>
<br/> <!-- 如果间隔太小，可以加一个空行 -->
```

<details><summary><b>点击展开</b></summary> 

// 代码块，注意上下都要保留空行

</details>


### 表格 (HTMl)
```html
<table style="width:80%; table-layout:fixed;">
    <tr>
        <th>th1</td>
        <th>th2</td>
    </tr>
    <tr>
        <td>td1</td>
        <td>td2</td>
    </tr>
</table>
```

<table style="width:80%; table-layout:fixed;">
    <tr>
        <th>th1</td>
        <th>th2</td>
    </tr>
    <tr>
        <td>td1</td>
        <td>td2</td>
    </tr>
</table>


## Latex
> 为确保在 GitHub 上生效, 在块前后增加空格或空行

```markdown
行内 $a+b=3$ 公式 (保证块前后有空格)

行内$a+b=3$公式 (没有空格可能会在一些解释器上失效)

单行居中 (保证块前后有空行, 否则可能在一些解释器上失效)

$$
    a+b=3
$$

> 更多语法见 [Latex 备忘](./LaTeX备忘.md)
```
行内 $a+b=3$ 公式 (保证块前后有空格)

行内$a+b=3$公式 (没有空格可能在一些解释器上可能失效)

单行居中 (保证块前后有空行, 否则可能在一些解释器上可能失效)

$$
    a+b=3
$$

> 更多语法见 [Latex 备忘](./LaTeX备忘.md)


### 引用
> 非标准用法，在编辑时不支持跳转，但是转换成 HTML 页面后可以；
>> 推荐使用[注脚](#注脚-footnotes)

```markdown
百度[$^{[1]}$](#ref1)是一种搜索引擎

<a name="ref1"> $[1]$ </a> [百度一下](https://www.baidu.com) <br/>
```

百度[$^{[1]}$](#ref1)是一种搜索引擎

<a name="ref1"> $[1]$ </a> [百度一下](https://www.baidu.com) <br/>

### 对齐

```markdown
$$
\begin{aligned}
    a &= 1 \\
    b &= 2
\end{aligned}
$$
```

$$
\begin{aligned}
    a &= 1 \\
    b &= 2
\end{aligned}
$$


## VSCode 插件

### 自动更新目录插件
- 插件名称：Markdown All in One
- 插入目录快捷键： `Shift + Command + P` (Create Table of Contents)
