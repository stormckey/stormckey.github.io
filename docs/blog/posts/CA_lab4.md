---
comments: true
authors:
    - stormckey
categories:
    - Lab
    - 计算机体系结构
date: 2023-11-30
nostatistics: true
---

# 计算机体系结构 - lab4  Cache

!!! abstract
    介绍一下实验中Cache设计的思想,从模块抽象的层面讲讲各模块的任务和交互的逻辑.

<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-arch.pages.zjusct.io/arch-fa23/lab4/)

本次实验是要实现一个cache,具体来说,会实现一个CMU(Cache Management Unit)来完成CPU, Memory, Cache之间的交互和控制,结构如下:

![](images/CA_lab4/2023-11-30-16-37-25.png#pic)

## Memory

在本实验中 Memory 只与 CMU交互.

Memory 与 CMU 的交互的方式只有一种:

- CMU 把读写需要的地址和数据给 Memory, Memory 进行读写操作然后返回数据给 CMU

## Cache

Cache 内部维护着所有Cache line的内容, 并且与CMU进行交互,主要的内容有两种:

<div class="annotate" markdown>

- 返回部分控制信息给CMU,包括
    - 是否命中
    - 被替换的Cache line是否有效且脏
    - 被写回的Cache line的tag(这样CMU才能获得正确的地址, 然后把数据写回Memory)
- 执行CMU要求的操作,包括:
    - load: 也就是从命中(1)Cache line中读信息和标记(LRU),返回
    - edit: 也就是对命中的Cache line进行修改和标记(LRU, dirty),返回
    - store: 将CMU的给的数据替换进Cache line,并且标记(valid, dirty, tag), 返回
    - invalid: 清空Cache

</div>

1.  命中了哪个Cache line或者哪个都没命中由Cache内部逻辑分辨.如果都没命中Cache此周期就啥都不干, 只返回控制信号, 等待CMU后续控制

为了做好这些事,Cache内部会进行实现合适的组合逻辑来进行索引,比较等等

## CPU

CPU 与 CMU 交互的方式有两种:

- CPU需要访存,将读写地址和数据给CMU
- CPU还会接受CMU的等待信号,阻塞流水线等待数据就位

## CMU

CMU内部维护一个状态机,这个状态机会根据上述三个组件的控制信号进行跳转:

- CPU是否有读写请求
- Memory对读写请求的处理
- Cache的控制信号反映Cache是命中了,需要访存还是需要写回

同时CMU也会根据自己的状态,对上述三个组件进行控制:

<div class="annotate" markdown>
- CPU是否应该stall(1)
- Cache要执行哪个操作(2)
- Memory要执行哪个操作(3)
</div>

1.  具体来说,下个state不是IDLE就该stall了
2.  -   load
    -   edit
    -   store
    -   invalid
3.  读写操作