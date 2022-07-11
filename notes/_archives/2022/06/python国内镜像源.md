Python 国内镜像源
===

- [pip](#pip)
    - [生效方法](#生效方法)
    - [国内源](#国内源)
- [conda](#conda)
    - [生效方法](#生效方法-1)
    - [清华源](#清华源)
    - [其他源](#其他源)

---

## pip

### 生效方法
```shell
# 安装时指定
pip install $pkg -i $channel

# 设置源
pip config set global.index-url $channel

# 删除源
pip config unset global.index-url
```

### 国内源
```shell
# 清华源
https://pypi.tuna.tsinghua.edu.cn/simple

# 阿里云
https://mirrors.aliyun.com/pypi/simple

# 中国科学技术大学 
https://pypi.mirrors.ustc.edu.cn/simple

#豆瓣
http://pypi.douban.com/simple
```

## conda

### 生效方法
```shell
# 安装时指定（推荐）
conda install $pkg -c $channel

# 添加源
conda config --set show_channel_urls yes  # 执行一次
conda config --add channels $channel

# 删除源
conda config --remove channels $channel
```

### 清华源
```shell
# main
https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/

# special
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
https://mirrors.tuna.tsinghua.edu.cn/tensorflow/linux/cpu/
```

### 其他源
- 豆瓣源
- 阿里源
- ...