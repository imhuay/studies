Markdown 简历工具
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-12-15%2023%3A40%3A41&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

<!-- TOC -->
- [GitHub 项目](#github-项目)
    - [komomoo/vuepress-theme-resume](#komomoovuepress-theme-resume)
    - [CyC2018/Markdown-Resume](#cyc2018markdown-resume)
- [网页版](#网页版)
- [简历技巧](#简历技巧)
<!-- TOC -->

## GitHub 项目

### komomoo/vuepress-theme-resume
> [komomoo/vuepress-theme-resume: 🐈 书写简洁优雅的前端程序员 markdown 简历，由 vuepress 驱动](https://github.com/komomoo/vuepress-theme-resume)

使用步骤
- [安装 nodejs](../12/nodejs环境.md#nodejs-环境搭建)
- 克隆本项目
```shell
nvm use 16  # 高版本可能报错

# 安装 yarn
npm install --global yarn

# git clone 仓库
git clone https://github.com/komomoo/vuepress-theme-resume.git
cd vuepress-theme-resume

# git remote 自己的仓库地址，因为 fork 的仓库不能设为私有仓库，故采用这种方式
git remote set-url origin git@github.com:imhuay/vuepress-theme-resume.git
git push

# 添加原仓库地址，以便更新
git remote add author git@github.com:komomoo/vuepress-theme-resume.git
git pull author master

# 安装依赖包
yarn # 或 npm i

# 开始
yarn dev # 或 npm run dev

# 编辑位置：example/README.md
```

### CyC2018/Markdown-Resume
> [CyC2018/Markdown-Resume: ⭐️ Markdown 简历模版](https://github.com/CyC2018/Markdown-Resume)


## 网页版
- [冷熊简历](http://cv.ftqq.com/)
- [木及简历](https://www.mujicv.com/)


## 简历技巧
- [怎么写好一份简历(算法工程师)](./_archives/2022/10/简历技巧.md)