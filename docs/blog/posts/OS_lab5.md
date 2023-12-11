---
comments: true
authors:
    - stormckey
categories:
    - OS
    - Lab
date: 2023-12-10
nostatistics: true
---

# 操作系统 - lab5 Demand Paging
!!! abstract
    一些踩过的坑，以及一个 kernel 执行流程总结
<!-- more -->

## kernel 执行流程

<div class="annotate" markdown>
```title="kernel 执行流程" hl_lines="8 14-18" linenums="0"
- `opensbi` 执行完毕
- `_start`: 完成 stvec， sie， mtimecmp， sstatus 和栈的设置，然后依次调用以下函数
    - `setup_vm`: 填写页表
    - `relocate`: 用设置好的页表修改 satp， 启动虚拟内存
    - `mm_init`: 完成内存分配函数的初始化
    - `setup_vm_final`: 切换到新的页表
    - `task_init`: 初始化进程
        - 对于 idle 以外的线程，在task_struct中添加stack和segment-01(1)对应的两段vma
- `start_kernel`: 不进入 test 等时钟中断，而是直接调用 schedule 调度走
- `schedule`: 根据policy选择下一个要调度的线程,调用 switch_to 至该线程
- `switch_to`: 获取先后线程的PCB地址，调用__switch_to
- `__switch_to`: 当前上下文存入 PCB，加载下一个进程的 PCB
- `__dummy`: 切用户栈，sret 返回用户段，而 sepc 是我们初始化的时候就指定的的 USER_START
- `ENTRY`: PC跳转至ENTRY，但是此时该页的映射并未完成，PAGE FAULT
- `_traps`: PAGE FAULT，保存上下文进入trap_handler
- `trap_handler`: 确认是PAGE FAULT后，调用do_page_fault
- `do_page_fault`: 根据current的vma确认是段错误、文件页缺页还是匿名页缺页，分配新页，填写内容(2)，填写页表，返回
- `_traps`: 恢复上下文返回，此后对应页已有映射
- `ENTRY`: 恢复执行，此后调度或者遇到新的缺页均同上处理
```
</div>

1.  也即readelf时得到的segment-01，包括.text .rodata .bss
2.  清零或者拷贝文件内容

## 栈切换问题

文档中指出，由用户发起的中断，我们需要在`_traps`开头切换到内核栈，但是对于内核发起的中断就不需要。而要判断中断是否由内核发起就要判断`sscratch`是否为0，在lab4中我把t0压栈后用t0来检验。

但是在lab5中这一方法行不通，因为当我们试图把t0压栈的时候我们的栈可能根本就是没分配的用户栈，那么这个压栈的行为只会引发新的PAGE FAULT，如此永远循环。

为了寻找解决方法可以先试图去查看linux时如何解决这一问题的，这是对应的[:octicons-code-16:代码](https://elixir.bootlin.com/linux/v6.0/source/arch/riscv/kernel/entry.S#L27)

可以看到linux使用了tp（thread pointer）以及指令`csrwr`,前者倒不是必要的使用，我们主要关注到`csrwr`指令可以实现csr与其他寄存器的交换，从而我们sp与`sscratch`的切换就不需要其他寄存器了，这就是正确的解决方式。

## PAGE FAULT

处理缺页异常时要仔细处理文件页的复制问题，如果要复制的一页中既有file_content，也有一些不在file之中的（如bss段），我们就需要分别处理这两段，前者复制，后者清零。

以下是一种处理思路：

- 无论如何，清零新页
- 找到`bad_addr`所在页的开头和结尾为默认的拷贝起地址和终地址
- 起地址不应小于文件内容开头地址`vm_start`
- 起地址不应大于文件内容结尾地址`vm_start + vm_content_size_in_file`
- 终地址不应大于文件内容结尾地址`vm_start + vm_content_size_in_file`
- 拷贝

## vmas

在kernel终，我们分配了一整页，其中的低地址放了个task_struct，高地址就是栈顶（如下图，来自实验文档）。所以我们要稍微限制一下vmas的大小，不能把分配的一页全给用了，还要留点给栈用。

```
                    ┌─────────────┐◄─── High Address
                    │             │
                    │    stack    │
                    │             │
                    │             │
              sp ──►├──────┬──────┤
                    │      │      │
                    │      ▼      │
                    │             │
                    │             │
                    │             │
                    │             │
    4KB Page        │             │
                    │             │
                    │             │
                    │             │
                    ├─────────────┤
                    │             │
                    │             │
                    │ task_struct │
                    │             │
                    │             │
                    └─────────────┘◄─── Low Address
```
