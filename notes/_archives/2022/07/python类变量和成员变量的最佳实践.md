类变量、成员变量，与注解
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [摘要](#摘要)
- [基本使用](#基本使用)
- [最佳实践](#最佳实践)
- [参考](#参考)

---

## 摘要
- Python 对定义在**类体**内的变量属于**类变量**还是**成员变量**（下称**实例变量**）的区分并不十分明确，这里记录一下我了解到的最佳实践。
    > 以 `self.x` 形式定义的就是成员变量，没有歧义；
- 定义在类内的变量，即是类变量，也是成员变量；因为两个同名的变量会分别被定义在了类和实例的 `__dict__` 中；它们之间除了同名没有其他关系；
    > 实例变量在被修改前并不会被真的定义出来，而是访问同名的类变量（相当于默认值）；一旦被修改，就会立即在实例中创建一个同名的实例变量，将两者隔离开来；
- 因此正确的做法是，通过**实例对象**访问那就是实例变量，通过**类对象**访问的就是类变量；
    ```python
    class A:
        x: int = 1

    a = A()
    print(A.x)  # 1  # 类变量
    print(a.x)  # 1  # 实例变量（此时并没有被真的创建，而是调用类变量作为默认值）
    print('x' in a.__dict__)  # False  # 实例变量并没有被真的定义出来

    a.x += 1  # 实例变量被修改
    print(A.x)  # 1  # 类变量
    print(a.x)  # 2  # 实例变量
    print('x' in a.__dict__)  # True  # 实例变量一旦被修改，就会立即被创建出来
    ``` 


## 基本使用
- 下面是一段来自官方的代码：
    ```python
    class BasicStarship:
        captain: str = 'Picard'               # instance variable with default
        damage: int                           # instance variable without default
        stats: ClassVar[Dict[str, int]] = {}  # class variable
    ``` 
    > [PEP 526 – Syntax for Variable Annotations | peps.python.org](https://peps.python.org/pep-0526/#class-and-instance-variable-annotations)
- `captain` **应该**是“类变量”（因为保存在 `BasicStarship.__dict__` 中），但官方的注释却是“实例变量”（成员变量）。
- 我理解其中的逻辑**可能**是这样的：
    - 记 `bs = BasicStarship()`；
    - 以 `bs.captain` 的方式访问 `captain`，会按照 `bs.__dict__ -> BasicStarship.__dict__` 的路径依次查找；
    - 而任何通过 `bs.captain` 对 `captain` 的修改，都会在 `bs` 中添加一个新的成员变量，同时不会影响 `BasicStarship.captain`
        ```python
        bs = BasicStarship()
        print(bs.captain)                # Picard
        print(BasicStarship.captain)     # Picard
        print('captain' in bs.__dict__)  # False

        bs.captain += '_local'           # setattr(bs, 'captain', BasicStarship.captain + '_local')
        print(bs.captain)                # Picard_local
        print(BasicStarship.captain)     # Picard
        print('captain' in bs.__dict__)  # True
        ``` 
<!-- - 所以可以认为在定义阶段区分**类变量**还是**成员变量**是没有意义的（`ClassVar` 注释也只是辅助，并不会影响运行时），而应该从变量的行为上看属于哪种变量； -->
- 所以我认为定义在类体内的变量（已初始化），即是类变量，也是实例变量；因为它被分别定义在了类和实例的 `__dict__` 中（虽然实例变量没有被立即定义），它们之间除了同名之外没有其他关系；
- 因此正确的做法应该是，通过**实例对象**访问那就是实例变量（`bs.captain`），通过**类对象**访问的就是类变量（`BasicStarship.captain`）；


## 最佳实践
TODO


## 参考
- [对象注解属性的最佳实践 — Python 官方文档](https://docs.python.org/zh-cn/3/howto/annotations.html)
- [PEP 526 – Syntax for Variable Annotations | peps.python.org](https://peps.python.org/pep-0526/#class-and-instance-variable-annotations)