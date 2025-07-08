huggingface 套件使用备忘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> ***Keywords**: huggingface*

<!--START_SECTION:toc-->
- [组件](#组件)
    - [transformers](#transformers)
    - [PEFT](#peft)
- [案例](#案例)
<!--END_SECTION:toc-->


## 组件
> [Hugging Face - Documentation](https://huggingface.co/docs)

### transformers
> 模型库
- 文档: [Transformers Doc](https://huggingface.co/docs/transformers/index)
- 仓库: [huggingface/transformers: 🤗 Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.](https://github.com/huggingface/transformers)


### PEFT
> Parameter-Efficient Fine-Tuning (PEFT)
>> 训练模型时只微调部分参数, 常见方法: LoRA, P-Tuning, Prefix Tuning 等;
- 文档: [PEFT Doc](https://huggingface.co/docs/peft/index)
- 仓库: [huggingface/peft: 🤗 PEFT: State-of-the-art Parameter-Efficient Fine-Tuning.](https://github.com/huggingface/peft)

LoRA: LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS
Prefix Tuning: Prefix-Tuning: Optimizing Continuous Prompts for Generation, P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks
P-Tuning: GPT Understands, Too
Prompt Tuning: The Power of Scale for Parameter-Efficient Prompt Tuning
AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning

## 案例
- [tloen/alpaca-lora: Instruct-tune LLaMA on consumer hardware](https://github.com/tloen/alpaca-lora)
    > 使用 lora 微调 alpaca;

