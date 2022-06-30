# conda 国内镜像源

## 修改方法
```shell
# 安装时指定（推荐）
conda install $pkg -c $channel

# 添加源
conda config --set show_channel_urls yes  # 执行一次
conda config --add channels $channel

# 删除原
conda config --remove channels $channel
```

## 清华源
```shell
# main
https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/

# special
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
https://mirrors.tuna.tsinghua.edu.cn/tensorflow/linux/cpu/
```

## 其他源
- 豆瓣源
- 阿里源
- ...