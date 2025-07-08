`git-subtree` 的基本用法
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [基本用法](#基本用法)
    - [Tips](#tips)
- [使用场景](#使用场景)
    - [场景1：从主仓库分出子仓库](#场景1从主仓库分出子仓库)
    - [场景2：将子仓库添加到主仓库](#场景2将子仓库添加到主仓库)
    - [场景3：删除子仓库](#场景3删除子仓库)
    - [强制推送子仓库](#强制推送子仓库)
    - [注意事项](#注意事项)
- [常见报错](#常见报错)
    - [`git subtree split` 时报 `Merge with strategy ours failed.`](#git-subtree-split-时报-merge-with-strategy-ours-failed)

---
- 参考文档
    - [git subtree教程 - SegmentFault 思否](https://segmentfault.com/a/1190000012002151)


## 基本用法

```shell
# 关联远程仓库
> git remote add $sub_repo_name $remote_url

# 将远程仓库作为子仓库添加到当前仓库
> git subtree add --prefix=$prefix $sub_repo_name $sub_repo_branch [--squash]

# 拉取子仓库
> git subtree pull --prefix=$prefix $sub_repo_name $sub_repo_branch [--squash]

# 将当前仓库下与 $prefix 目录有关的提交提取到单独的分支
> git subtree split --prefix=$prefix --branch $sub_branch [--rejoin [--squash]]

# 推送子仓库
> git subtree push --prefix=$prefix $sub_repo_name $sub_repo_branch [--rejoin [--squash]]
```
变量说明：
- `$prefix`：子仓库在主仓库的路径
- `$sub_repo_name`：子仓库的别名
- `$remote_url`：子仓库的远程地址
- `$sub_repo_branch`：子仓库的推送/拉取分支，一般为 master
- `$sub_branch`：子仓库在主仓库中分离出来的分支，一般取子仓库所在的目录名

选项说明：
- `--squash`：“merge subtree changes as a single commit”；
    - **使用前提**：主/子仓库不能有待提交的 commit；
    - 对 `split` 和 `push` 命令，必须在 `--rejoin` 下才能使用；
- `--rejoin`：“merge the new branch back into HEAD”
    - **使用前提**：主/子仓库不能有待提交的 commit；
    - 效果：建立一个新的起点，避免从头开始遍历与子仓库相关的提交；
    - 建议配合 `--squash` 一起使用；

### Tips
- 如果长时间没有 `--rejoin`，可能导致遍历时间过长，甚至超过内存上限导致奔溃；
- `--rejoin` 的时候建议带上 `--squash`，否则会导致所有与子仓库相关的 commit 都重新提交一次，进而污染 commit 日志；
    > [git subtree使用体验 - 问题2](https://blog.csdn.net/huangxiaominglipeng/article/details/111195399)


## 使用场景

### 场景1：从主仓库分出子仓库

1. 关联子仓库与 git 地址（一般为空仓库）：`git remote add $name xxx.git`
2. 将子仓库提取到单独的分支：`git subtree split --prefix=$prefix --branch $name --rejoin`
3. 推送子仓库代码：`git subtree push --prefix=$prefix $name master --squash`

> 推荐在每次 push 子仓库代码时，都 `git subtree split --rejoin` 一次； <br/>
> 因为当主项目的 commit 变多后，再推送子项目到远程库的时候，subtree 每次都要遍历很多 commit；
>> 解决方法就是使用 split 打点，作为下次遍历的起点。解决这个问题后就可以彻底抛弃 `git submodule` 了；
>>> [git subtree使用体验_李棚的CSDN专栏](https://blog.csdn.net/huangxiaominglipeng/article/details/111195399)

### 场景2：将子仓库添加到主仓库

1. 关联子仓库与 git 地址：`git remote add $name xxx.git`
2. 设置子仓库路径（第一次执行时会自动拉取代码）：`git subtree add --prefix=$prefix $name master --squash`
3. 拉取子仓库代码：`git subtree pull --prefix=$prefix $name master --squash`

### 场景3：删除子仓库
1. 切断子仓库关联：`git remote remove $name`
2. 删除子仓库：`rm -r $prefix`

### 强制推送子仓库
> [How do I force a subtree push to overwrite remote changes? - Stack Overflow](https://stackoverflow.com/questions/33172857/how-do-i-force-a-subtree-push-to-overwrite-remote-changes)  
**使用场景**：有时因为 rebase 等操作导致远程子仓库与本地不一致，而 `git subtree push` 并不支持 `--force` 选项，导致推送失败；

**命令**：
```sh
git push --force $name `git subtree split --prefix=$prefix --branch $name --rejoin`:$remote_branch
# 等价于 git push --force $name $commit_id:$remote_branch
# --force 强制推送
# $name: 子仓库远程地址的别名
# $remote_branch: 子仓库远程目标分支，一般为 master 或 main
```

### 注意事项
- 不要对 git subtree split 产生的 commit 进行 rebase/merge 操作，会导致文件错乱！


## 常见报错

### `git subtree split` 时报 `Merge with strategy ours failed.`

- **完整命令**：`git subtree split --prefix=$prefix --branch $name --rejoin`
- **原因**：本地有文件还没提交；