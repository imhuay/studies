git-删除历史已提交文件
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-08-02%2000%3A35%3A22&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: git*

<!--START_SECTION:toc-->
- [背景](#背景)
- [操作方法](#操作方法)
    - [基于 `git filter-branch`](#基于-git-filter-branch)
    - [基于 BFG Repo-Cleaner](#基于-bfg-repo-cleaner)
<!--END_SECTION:toc-->


## 背景

从Git历史中删除包含敏感信息的文件

## 操作方法

### 基于 `git filter-branch`

```bash
# 备份仓库, 在备份仓库上操作
git clone --mirror your-repo.git  # 克隆所有分支、标签、refs（包括远程跟踪分支）的完整镜像
cd your-repo.git

# 运行filter-branch命令（将 [target-file] 替换为目标文件）
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch [target-file]' \
--prune-empty --tag-name-filter cat -- --all

# 清理和推送更改
git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 强制推送到远程仓库
git push origin --force --all
git push origin --force --tags
```


### 基于 BFG Repo-Cleaner
> [BFG Repo-Cleaner by rtyley](https://rtyley.github.io/bfg-repo-cleaner/)

```bash
git clone --mirror your-repo.git
cd your-repo.git

java -jar bfg.jar --delete-files path/to/sensitive/file
# bfg --delete-files path/to/sensitive/file

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```