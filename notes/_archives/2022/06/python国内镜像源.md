python 国内镜像源
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-06-08%2023%3A49%3A14&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: python*

<!--START_SECTION:toc-->
- [pip](#pip)
- [conda](#conda)
<!--END_SECTION:toc-->



## pip

```shell
# 安装时指定
pip install $pkg -i https://mirrors.aliyun.com/pypi/simple

# 设置源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com

# 删除源
pip config unset global.index-url
pip config unset install.trusted-host
```

**国内源**
- 清华源: `https://pypi.tuna.tsinghua.edu.cn/simple`
- 阿里: `https://mirrors.aliyun.com/pypi/simple`
- 豆瓣: `http://pypi.douban.com/simple`
- pypi 源列表（校园网联合镜像站）：https://mirrors.cernet.edu.cn/list/pypi


## conda

```shell
# 安装时指定（推荐）
conda install $pkg -c $channel

# 添加源
conda config --set show_channel_urls yes  # 执行一次
conda config --add channels $channel

# 删除源
conda config --remove channels $channel
```

**国内源**
```shell
# 清华源
# main
https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
# special
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
https://mirrors.tuna.tsinghua.edu.cn/tensorflow/linux/cpu/
```
