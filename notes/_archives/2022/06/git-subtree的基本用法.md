`git-subtree` 的基本用法
===

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