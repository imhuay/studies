Linux 后台执行
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [`&` 指令（需要保持终端运行）](#-指令需要保持终端运行)
    - [`>/dev/null 2>&1` 详解](#devnull-21-详解)
- [`nohup` 指令（不需要保持终端运行）](#nohup-指令不需要保持终端运行)
    - [关闭进程](#关闭进程)
- [把执行中的命令转到后台](#把执行中的命令转到后台)

---

## `&` 指令（需要保持终端运行）

- 命令格式：`[command] &`；<br/>
    但此时标准输出还是会显示到当前终端，非常影响操作，所以一般需要配合重定向输出来使用；如<br/>

    ```shell
    [command] >/dev/null 2>&1 &
    ```

    或者

    ```shell
    [command] &>/dev/null &
    ```

    > `&>file` 等价于 `>file 2>&1`，表示把“标准输出”和“标准错误输出”都重定向到文件 file


### `>/dev/null 2>&1` 详解
1. `>` 表示输出重定向，如 `echo "123" > ~/123.txt`；
1. `/dev/null` 代表空设备文件，相当于丢弃输出；
1. `2` 表示 stderr 标准错误输出；
1. `&` 在这里表示“引用”，即表示`2`的输出重定向跟 `1` 相同；
1. `1` 表示 stdout 标准输出，是系统默认，可以省略，因此 `>/dev/null` 相当于 `1>/dev/null`
1. 除了将输出重定向到`/dev/null`，还可以重定向到自定义文件，如`>log.txt 2>&1`、`>out.txt 2>err.txt`

## `nohup` 指令（不需要保持终端运行）
- 命令格式：`nohup [command] &`；
    - `nohup` 命令会忽略 SIGHUP 信号，从而终端退出时不会影响到后台作业；
    - 通过 `nohup` 运行的程序，其输出信息将不会显示到终端，默认输出到当前目录的 `nohup.out` 文件中；如果当前目录的 `nohup.out` 文件不可写，则输出重定向到 `$HOME/nohup.out` 文件中；
    - 也可以指定输出文件，如 `nohup [command] &>log.txt &`

### 关闭进程
- 如果还没有关闭终端
    - 使用 `jobs -l` 找到 job id；
- 如果已经关闭终端
    - 使用 `ps -aux | grep $keyword` 查找进程 id；


## 把执行中的命令转到后台
1. `Ctrl+Z`：将当前在前台执行的程序在后台挂起；<br/>
    `Ctrl+C`：前台进程终止；
1. `bg %n` 将在后台挂起的进程，在**后台**继续执行；<br/>
    `fg %n` 将在后台挂起的进程，在**前台**继续执行；<br/>
    `kill %n` 杀死后台挂起的进程；
    > 其中 `n` 为 job id
1. `jobs`：查看在后台执行的进程；第一列在 `[]` 中的数字即为 job id；

    ``` shell
    -> % jobs
    [1]    running    sh test.sh &> /dev/null
    [2]  - suspended  sh test.sh
    [3]  + suspended  sh test.sh
    ```
