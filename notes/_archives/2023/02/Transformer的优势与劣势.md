Transformer 的优势与劣势
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-02-02%2016%3A35%3A31&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: true
-->

> ***Keywords**: transformers*

<!--START_SECTION:toc-->
- [References](#references)
<!--END_SECTION:toc-->


## References
- [Transformer升级之路：8、长度外推性与位置鲁棒性 - 科学空间|Scientific Spaces](https://kexue.fm/archives/9444)
    - “这里的che基准就是测试模型是否具有解析正则语言、上下文无关语言、以及上下文有关语言语义的能力吧，也就是看神经模型能不能模拟有限状态机、下推自动机以及线性有界自动机。对这三种语言的解析transformer相比rnn是有天然劣势的，其原因就是注意力机制的无序性以及作为补偿的位置编码的次优性，用这三种语言比较rnn和transformer的话后者确实吃亏的。自然语言跟这三种语言明显不一样，众多实践已经证明transformer的自然语言语义解析能力远大于rnn的。这就带来一个问题：用che基准衡量transformer长度外推能力所得到的优劣结论，可以作为其对自然语言长度外推能力的有效参考吗？” —— 李子涵