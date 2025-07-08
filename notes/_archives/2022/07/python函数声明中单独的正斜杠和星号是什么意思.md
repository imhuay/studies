Python 函数声明中单独的正斜杠（/）和星号（*）是什么意思
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

```python
def func(a, /, b, *, c):
    print(a, b, c)

func(1, 2, c=3)  # ok
func(1, b=2, c=3)  # ok
func(a=1, 2, 3)  # err
```
- `/` 规定了在其之前的参数都必须是 **positional argument**，而不能是 **keyword argument**；之后的不管，两种均可；
- `*` 规定了在其之后的参数都必须是 **keyword argument**，而不能是 **positional argument**；之前的不管，两种均可；
- 当两者同时出现时，`/` 必须在 `*` 之前；


## 使用示例
```python
def f1(a, b, c, /):  # ok
    pass

f1(1, 2, 3)  # ok
f1(1, 2, c=3)  # err


def f2(*, a, b, c):  # ok
    pass

f2(a=1, b=2, c=3)  # ok
f2(1, b=2, c=3)  # err


def f3(a, /, *, b):  # ok
    pass

f3(1, b=2)  # ok
f3(1, 2)  # err
f3(a=1, b=2)  # err


def f4(a, /, b, *, c):  # ok
    pass

f4(1, 2, c=3)  # ok
f4(1, b=2, c=3)  # ok
f4(1, 2, c)  # err
f4(a=1, b=2, c=3)  # err


def f5(a, *, b, /, c):  # err: invalid syntax
    pass
```