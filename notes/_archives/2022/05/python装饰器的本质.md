装饰器的本质
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- **装饰器**（不带参数的装饰器）从实现上看，就是一个“输入和输出都是**函数对象**”的函数；
- **带参数的装饰器**实际上就是一个返回普通装饰器的函数（可以接受任意参数）；
- **装饰器语法**实际上就是以下两种调用形式的语法糖：
    ```python
    # 不带参数
    func = decorator(func)
    # 带参数
    func = decorator(*args)(func)
    ```
- **类装饰器**同理，就是一个“输入和输出都是**类对象**”的函数，也是类似的语法糖；
    ```python
    # 不带参数
    clas = decorator(clas)
    # 带参数
    clas = decorator(*args)(clas)
    ```
- **装饰器类**：具有装饰器功能的类，通过重载 `__call__` 实现；

---

- [`示例 1`：装饰器（不带参数）](#示例-1装饰器不带参数)
- [`示例 2`：带参数的装饰器](#示例-2带参数的装饰器)
- [`示例 3`：`functools.wraps` 的作用](#示例-3functoolswraps-的作用)
- [`示例 4`：类装饰器](#示例-4类装饰器)
- [`示例 5`：装饰器类（不带参数）](#示例-5装饰器类不带参数)
- [`示例 6`：带参数的装饰器类](#示例-6带参数的装饰器类)

## `示例 1`：装饰器（不带参数）

1. 定义装饰器
    ```python
    def dn(fn):  # 输入是一个函数
        """一个简单的装饰器，打印被装饰函数的结果"""
        
        def wrapper(*args, **kwargs):
            ret = fn(*args, **kwargs)
            print(f'Result: {ret}')
            return ret  # 返回原函数的结果
            
        return wrapper  # 返回是一个函数
    ```
2. 调用装饰器
    ```python
    @dn
    def func(a, b):
        return a + b

    ret = func(1, 2)  # Result: 3
    print(ret)  # 3
    ```
3. 等价行为
    ```python
    def func(a, b):
        return a + b

    func = dn(func)

    ret = func(1, 2)  # Result: 3
    print(ret)  # 3
    ```

## `示例 2`：带参数的装饰器

1. 定义装饰器
    ```python
    def dn_pro(prefix):  # 普通函数，可以传入任意参数
        """自定义打印前缀"""

        def dn(fn):
            """一个简单的装饰器，打印被装饰函数的结果"""

            def wrapper(*args, **kwargs):
                ret = fn(*args, **kwargs)
                print(f'{prefix}: {ret}')
                return ret  # 返回原函数的结果

            return wrapper

        return dn  # 返回一个装饰器
    ```
2. 调用装饰器
    ```python
    @dn_pro('ret')
    def func(a, b):
        """"""
        return a + b
    ```
3. 等价行为
    ```python
    def func(a, b):
        return a + b

    func = dn_pro('ret')(func)

    ret = func(1, 2)  # ret: 3
    print(ret)  # 3
    ```

## `示例 3`：`functools.wraps` 的作用

- 在示例 2 中，打印 `func.__name__` 的结果是 `wrapper`；  
  这是因为经过装饰器后，`func` 实际上已经**指向**了另一个函数；
- 这时可以通过 `functools.wraps` 装饰器保留原函数的相关属性，用法如下：
    > `functools.wraps` 本身也是一个带参数的装饰器；

```python
import functools  # 导入 functools

def dn_pro(prefix):  # 普通函数，可以传入任意参数
    """自定义打印前缀"""

    def dn(fn):
        """一个简单的装饰器，打印被装饰函数的结果"""

        @functools.wraps(fn)  # 保留 fn 的相关属性
        def wrapper(*args, **kwargs):
            ret = fn(*args, **kwargs)
            print(f'{prefix}: {ret}')
            return ret  # 返回原函数的结果

        return wrapper

    return dn  # 返回一个装饰器

@dn_pro('ret')
def func(a, b):
    return a + b

print(func.__name__)  # func
```

## `示例 4`：类装饰器

- **类装饰器**就是一个“输入和输出都是**类对象**”的函数；

1. 定义一个类装饰器：给装饰的类添加一个 `printf` 函数
    ```python
    def dn(cls):
        def printf(self):
            print(self.__dict__)

        # cls.printf = printf
        setattr(cls, 'printf', printf)
        return cls
    ```
2. 调用装饰器
    ```python
    @dn
    class A:

        def __init__(self, a, b):
            self.a = a
            self.b = b


    a = A(1, 2)
    a.printf()  # {'a': 1, 'b': 2}
    ```
3. 等价行为
    ```python
    class A:

        def __init__(self, a, b):
            self.a = a
            self.b = b


    A = dn(A)

    a = A(1, 2)
    a.printf()  # {'a': 1, 'b': 2}
    ```


## `示例 5`：装饰器类（不带参数）

- 装饰器类：具有装饰器功能的类，通过重载 `__call__` 实现；
- 需要注意的是，该场景下不能使用 `functools.wraps`，而应该使用 `functools.update_wrapper`，详见示例；

1. 定义装饰器类
    ```python
    class Dn:

        def __init__(self, fn):
            functools.update_wrapper(self, fn)  # !
            self.fn = fn

        def __call__(self, *args, **kwargs):
            ret = self.fn(*args, **kwargs)
            print(f'Result:', ret)
            return ret
    ```
2. 调用装饰器类
    ```python
    @Dn
    def func(a, b):
        return a + b

    ret = func(1, 2)  # Result: 3
    print(ret)  # 3
    print(func.__name__)  # func
    ```
3. 等价行为
    ```python
    def func(a, b):
        return a + b

    func = Dn(func)
    
    ret = func(1, 2)  # Result: 3
    print(ret)  # 3
    print(func.__name__)  # func
    ```


## `示例 6`：带参数的装饰器类

1. 定义装饰器类
    ```python
    class Dn:

        def __init__(self, prefix):
            self.prefix = prefix

        def __call__(self, fn):

            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                ret = fn(*args, **kwargs)
                print(f'{self.prefix}:', ret)
                return ret

            return wrapper
    ```

2. 调用装饰器类
    ```python
    @Dn('ret')
    def func(a, b):
        return a + b

    ret = func(1, 2)  # ret: 3
    print(ret)  # 3
    print(func.__name__)  # func
    ```

3. 等价行为
    ```python
    def func(a, b):
        return a + b

    func = Dn('ret')(func)

    ret = func(1, 2)  # ret: 3
    print(ret)  # 3
    print(func.__name__)  # func
    ```
