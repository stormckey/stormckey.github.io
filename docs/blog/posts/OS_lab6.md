---
comments: true
authors:
    - stormckey
categories:
    - OS
    - Lab
date: 2023-12-11
nostatistics: true
---

# 操作系统 - lab6 fork
!!! abstract
    一些踩过的坑，以及一个 kernel 执行流程总结
<!-- more -->
!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-sec.github.io/os23fall-stu/lab6/)

## kernel 执行流程


<div class="annotate" markdown>
```title="kernel 执行流程" hl_lines="18-37" linenums="0"
- opensbi 执行完毕
- _start: 完成 stvec， sie， mtimecmp， sstatus 和栈的设置，然后依次调用以下函数
    - setup_vm: 填写页表
    - relocate: 用设置好的页表修改 satp， 启动虚拟内存
    - mm_init: 完成内存分配函数的初始化
    - setup_vm_final: 切换到新的页表
    - task_init: 初始化进程
- start_kernel: 不进入 test 等时钟中断，而是直接调用 schedule 调度走
- schedule: 根据 policy 选择下一个要调度的线程，调用 switch_to 至该线程
- switch_to: 获取先后线程的 PCB 地址，调用__switch_to
- __switch_to: 当前上下文存入 PCB，加载下一个进程的 PCB
- __dummy: 切用户栈，sret 返回用户段，而 sepc 是我们初始化的时候就指定的的 ENTRY
- ENTRY: PC 跳转至 ENTRY，但是此时该页的映射并未完成，PAGE FAULT
- _traps: PAGE FAULT，保存上下文进入 trap_handler
- trap_handler: 确认是 PAGE FAULT 后，调用 do_page_fault
- do_page_fault: 根据 current 的 vma 确认是段错误、文件页缺页还是匿名页缺页，分配新页，填写内容，填写页表，返回
- _traps: 恢复上下文返回，此后对应页已有映射
- ENTRY: 恢复执行，直到调用 fork
- _traps: 保存上下文，进入 trap_handler
- trap_handler: 确认是 fork 后，调用 sys_clone
- sys_clone: 进行一定的拷贝以初始化子进程，初始化完成后加入调度队列
    -  将父进程 kernel stack 所在页拷贝一份给子进程，其中包括
          - task_struct: 位于该页低地址，其中内容在__switch_to 到至子进程的时候会被加载，以下项需要改动
              - pid: 子进程的新 pid
              - thread.sp: 换到子进程后系统栈的起始地址，注意切换过来时栈内已有数据
              - thread.ra: __switch_to 到子进程后，__switch_to 函数结束，应该 ret 到子进程的__return_from_fork
              - thread.sscratch: 子进程在内核态的 sscratch，在返回用户态时会与 sp 交换，所以实质是子进程用户态的 sp (1)
              - satp: 根据子进程页表修改
              - pgd: 子进程页表
          - pt_regs: 位于该页高地址，其中内容在子进程从内核态返回用户态时将会被加载，以下项需要改动
              - a0: 返回用户态后携带的调用返回值，也就是子进程得到的 fork 返回值，0
              - sepc: fork 对应 ecall 的下一条指令
    - 将父进程的用户态页内容都拷贝一份给子进程，并在子进程的页表中添加这些页的映射
- _traps: 父进程 fork 完毕，携带子进程 pid 恢复用户态上下文返回 ecall 下一条指令
- fork: 回到用户态，继续执行父进程，打印信息直到被调度走，随后调度算法选择子进程
- __switch_to: 保存父进程上下文至父进程 task_struct,从子进程 task_struct 中恢复子进程内核态上下文(2)，ret 返回到__return_from_fork 继续执行用户态代码
- __return_from_fork: 子进程从 pt_regs 中恢复用户态上下文(3)，包括返回值 0，从 trap 返回 ecall 下一条指令，继续执行
```
</div>

1.  正常来说返回用户态的 sp 应该从 pt_regs 中恢复（文档中也是这么说的），但我实践上是从 sscratch 恢复的，这里应该根据具体实现修改。
2.  此处的上下文就是我们在 fork 中设置的
3.  此处的上下文就是我们在 fork 中设置的


## 调度算法

我们的 task 数组大小是`NR_TASKS`,所以我们要做到

- 只初始化指定数量的进程，而不是填满整个数组
- 调度的时候要遍历数组，但是只会调度那些有效的 task

## 返回值异常

如果忘了将子进程返回用户态的地址设置为 ecall 下一条，可能导致 fork 返回值异常。设想如下情况：

- idle 进程 pid 为 0，父进程为 1，子进程为 2
- 调度子进程后 sepc 指向 ecall，所以子进程返回用户态后继续执行 ecall
- 子进程执行 ecall 再次进行 fork，fork 出新的子进程，在此次 fork 中，父进程为 2，子进程为 3
- 2 进程完成 fork 返回，此时返回的是 ecall 的下一条（因为系统调用中会将 sepc+4），返回值为 3

可以看到 2 进程因为额外进行了一次 fork 所以返回值不再是其作为 1 的子进程拿到的 0，而是作为 3 的父进程拿到的 3，这就发生了错误
