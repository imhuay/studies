Markdown 备忘
===

- [插件](#插件)
    - [自动更新目录插件（VSCode）](#自动更新目录插件vscode)
- [编辑](#编辑)
    - [目录结构](#目录结构)
    - [换行](#换行)
    - [居中插入图片](#居中插入图片)
    - [隐藏块](#隐藏块)
    - [HTML 表格](#html-表格)
- [Latex](#latex)
    - [参考和引用](#参考和引用)
    - [公式对齐](#公式对齐)


## VSCode 插件

### 自动更新目录插件
- 插件名称：Markdown All in One
- 插入目录快捷键： `Shift + Command + P` (Create Table of Contents)


## 编辑

### 目录结构
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

### 居中插入图片

- 法1）使用 `<div>` 控制
    - 不带链接
        ```html
        <div align="center"><img src="./_assets/xxx.png" height="300" /></div>
        ```
    - 带链接
        ```html
        <div align="center"><a href=""><img src="./_assets/xxx.png" height="300" /></a></div>
        ```
        - `height`用于控制图片的大小，一般不使用，图片会等比例缩放；
- 法2）使用全局样式，不一定生效；
    ```html
    <style> 
    .test{width:300px; align:"center"; overflow:hidden} 
    .test img{max-width:300px;_width:expression(this.width > 300 ? "300px" : this.width);} 
    </style> 
    ``` 


### 隐藏块
```html
<details><summary><b>示例：动态序列（点击展开）</b></summary> 

// 代码块，注意上下都要保留空行

</details>
<br/> <!-- 如果间隔太小，可以加一个空行 -->
```


### HTML 表格
```html
<table style="width:80%; table-layout:fixed;">
    <tr>
        <th align="center">普通卷积</td>
        <th align="center">空洞卷积</td>
    </tr>
    <tr>
        <td><img width="250px" src="./res/no_padding_no_strides.gif"></td>
        <td><img width="250px" src="./res/dilation.gif"></td>
    </tr>
</table>
```

### Latex 语法
- 在 markdown 内使用：行内使用 `$` 包围，如 $a+b=3$；
- 独立代码块使用 `$$` 包围，如：
$$
    a+b=3
$$
- 更多语法见 [Latex 备忘](./LaTeX备忘.md)


### 上标引用
> 非标准用法，在编辑时不支持跳转，但是转换成 HTML 页面后可以；

示例：百度[$^{[1]}$](#ref1)是一种搜索引擎

<a name="ref1"> $[1]$ </a> [百度一下](https://www.baidu.com) <br/>

### 公式对齐

$$
\begin{aligned}
    a &= 1 \\
    b &= 2
\end{aligned}
$$