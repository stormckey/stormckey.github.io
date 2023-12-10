---
comments: true
authors:
    - stormckey
categories:
    - Lab
    - OS
date: 2023-11-25
nostatistics: true
---
# 操作系统 - lab3 虚拟内存
!!! abstract
    一些踩过的坑，以及一个 kernel 执行流程总结
<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-sec.github.io/os23fall-stu/lab3/)

## kernel 执行流程

<div class="annotate" markdown>
```title="kernel 执行流程" hl_lines="3-4 6" linenums="0"
- `opensbi`执行完毕
- `_start`: 完成 stvec， sie， mtimecmp， sstatus 和栈(1)的设置，然后依次调用以下函数
    - `setup_vm`: 填写页表(2)
    - `relocate`: 用设置好的页表修改 satp， 至此虚拟内存已经启动
    - `mm_init`: 完成内存分配函数的初始化
    - `setup_vm_final`: 利用 mm 中的函数分配新的页来设置多级分段页表，切换到新的页表(3)
    - `task_init`: 初始化进程
- `start_kernel`: 进入 test 死循环，等待被调度走
```
</div>

1.  注意要使用栈的物理地址，此时符号表里的都是虚拟地址
2.  注意这里跳填表要填直接映射和等值映射两段
3.  确定好不同段的物理虚拟地址和权限等，调用 creat_mapping 函数分配并填写页表，注意页表项均使用物理地址

## 注意事项

### 写 satp

我们启用虚拟内存的那一步，也就是写 satp 的那一步只是一句`csrw`，指令写完寄存器也不会干什么额外的事情，CP 还是要继续去 PC+4 执行下一条指令.

所以 PC+4 这个地址在虚拟内存下该怎么取指(1)，这个问题就是思考题所关心的.
{ .annotate }

1.  有对应的映射吗，或者是用中断处理？

### 为什么第一次我们启用的页表是一级的

文档中其实已经有链接指向了解释这一点的文档，具体而言，在这段描述转化虚拟内存的过程的[:octicons-book-16:手册](https://www.five-embeddev.com/riscv-isa-manual/latest/supervisor.html#sv32algorithm)中

仔细阅读，其中第四点提到若当前页表项的权限表明了可读或者可执行，那么就会当作是最后一级页表，否则才会把它当作某一级的页表

### debug 注意

- 当我们按照文档修改了链接文件后，我们 gdb 中直接用符号来打断点之类的操作就都是按照修改了链接文件之后的虚拟地址了，所以启用虚拟内存之前为了在正确的物理地址打断点，需要手动输入地址.
- 如果你跟我一样改完页表没事，但是一刷新 tlb 就寄了.于我的经验而言，是页表写的有问题.

