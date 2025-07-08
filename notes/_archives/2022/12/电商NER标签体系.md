电商 NER 标签体系
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-12-22%2020%3A10%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: true
-->

> 关键词: cross-border e-commerce (跨境电商), NER

<!-- TOC -->
- [常见标签](#常见标签)
- [标注准则](#标注准则)
    - [产品词/核心词](#产品词核心词)
    - [修饰成分和复合产品词的区别](#修饰成分和复合产品词的区别)
<!-- TOC -->


## 常见标签

- 类目词
- 修饰词/限定词
    - 风格
    - 颜色
    - 材质
    - 尺寸
    - 节日
    - 功能
    - 场景
- 核心词
    - 产品
- 品牌 (修饰 or 核心 ?)


## 标注准则

### 产品词/核心词
> query/title 中的核心成分
- 领域相关: 比如 "cat" 在宠物垂搜和综合电商场景下;
- 固定搭配, 如 "down jacket (羽绒服)", "fork bag (叉袋, 一种装在自行车上的骑行包)";
- 非固定搭配, 通过多种产品组合描述, 如 "phone stand (手机支架)", "stationery bag (文具袋)"

### 修饰成分和复合产品词的区别
> 判断一个短语应该整体作为一个产品词, 还是作为修饰词 + 产品词
>> 有些情况要看召回策略

- 复合产品词的几种情况:
    1. 固定搭配, 已经成为惯例用法, 如 "moon cake" (月饼);
    2. 两种或多种产品共同描述了一种产品, 如 "phone stand" (手机支架);
- 整体标注为一个产品词的几种情况;
    - 固定搭配;
    - 子类目; 如果专门为某类产品设计了子类目, 那么就应该整体标注为产品词;
    - 产品样式/使用场景发生了明显变化;
        - "shower shelf (浴架)", 建议作为一个整体;
        - "essential oil (精油)", 固定搭配;
        - "temper glass (钢化玻璃)";
        - "magic pen (魔术笔)";
        - "shark/duckbill clip (鲨鱼/鸭嘴发夹)", 可以作为一个整体, 也可以当做修饰 + 产品; 因为产品样式发生了变化, 当有修饰时, 已经明确了搜索目标; 当召回足够的情况下, 作为整体召回; 如果不够, 可以分开召回;
- 去掉修饰后, 产品样式是否发生变化;
    - shoulder bag 与 bag 有明显变化, 所以应该把 shoulder bag 当做一个整体;
- 有时从定义上难以区分时, 需要参考搜索结果;
- 一般 修饰词 + 产品词 的情况, 可以在中间插入其他修饰

示例
```
产品词 (下位词):
    lariat necklace (套索项链)
    shoulder bag (单肩包)
    slide sandals (拖鞋)
    activated carbon (活性炭)
    moon cake (月饼)
    shower rug (吸水毯)

修饰 + 产品:
    zipper (拉链, 风格) purse (钱包)
    ceramic (陶瓷, 材质) knife (刀)
    washable (水洗, 功能) rug (地毯)
    colorblock (拼色, 风格) dress (裙子)

待定:
    combination lock (密码锁)
```

