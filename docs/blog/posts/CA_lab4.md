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
    介绍一下实验中 Cache 设计的思想，从模块抽象的层面讲讲各模块的任务和交互的逻辑。

<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-arch.pages.zjusct.io/arch-fa23/lab4/)

本次实验是要实现一个 cache,具体来说，会实现一个 CMU(Cache Management Unit)来完成 CPU, Memory, Cache 之间的交互和控制，结构如下：

![](images/CA_lab4/2023-11-30-16-37-25.png#pic)

## Memory

在本实验中 Memory 只与 CMU 交互。

Memory 与 CMU 的交互的方式只有一种：

- CMU 把读写需要的地址和数据给 Memory, Memory 进行读写操作然后返回数据给 CMU

## Cache

Cache 内部维护着所有 Cache line 和标记位，并且与 CMU 进行交互，主要的内容有两种：

<div class="annotate" markdown>

- 返回部分控制信息给 CMU,包括
    - 是否命中
    - 被替换的 Cache line 是否有效且脏
    - 被写回的 Cache line 的 tag（这样 CMU 才能获得正确的地址，然后把数据写回 Memory）
- 执行 CMU 要求的操作，包括
    - load: 也就是从命中(1)Cache line 中读信息和标记(LRU),返回
    - edit: 也就是对命中的 Cache line 进行修改和标记(LRU, dirty),返回
    - store: 将 CMU 的给的数据替换进 Cache line,并且标记(valid, dirty, tag), 返回
    - invalid: 清空 Cache

</div>

1.  命中了哪个 Cache line 或者哪个都没命中由 Cache 内部逻辑分辨.如果都没命中 Cache 此周期就啥都不干，只返回控制信号，等待 CMU 后续控制

为了做好这些事，Cache 内部会进行实现合适的组合逻辑来进行索引，比较等等

## CPU

CPU 与 CMU 交互的方式有两种：

- CPU 需要访存，将读写地址和数据给 CMU
- CPU 还会接受 CMU 的等待信号，阻塞流水线等待数据就位

## CMU

CMU 内部维护一个状态机，这个状态机会根据上述三个组件的控制信号进行跳转：

- CPU 是否有读写请求
- Memory 对读写请求的处理
- Cache 的控制信号反映 Cache 是命中了，需要访存还是需要写回

同时 CMU 也会根据自己的状态，对上述三个组件进行控制：

<div class="annotate" markdown>
- CPU 是否应该 stall(1)
- Cache 要执行哪个操作(2)
- Memory 要执行哪个操作(3)
</div>

1.  具体来说，下个 state 不是 IDLE 就该 stall 了
2.  -   load
    -   edit
    -   store
    -   invalid
3.  读写操作
