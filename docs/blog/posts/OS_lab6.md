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

## kernel 执行流程

<div class="annotate" markdown>
```title="kernel 执行流程" hl_lines="18-36" linenums="0"
- `opensbi` 执行完毕
- `_start`: 完成 stvec， sie， mtimecmp， sstatus 和栈的设置，然后依次调用以下函数
    - `setup_vm`: 填写页表
    - `relocate`: 用设置好的页表修改 satp， 启动虚拟内存
    - `mm_init`: 完成内存分配函数的初始化
    - `setup_vm_final`: 切换到新的页表
    - `task_init`: 初始化进程
- `start_kernel`: 不进入 test 等时钟中断，而是直接调用 schedule 调度走
- `schedule`: 根据policy选择下一个要调度的线程,调用 switch_to 至该线程
- `switch_to`: 获取先后线程的PCB地址，调用__switch_to
- `__switch_to`: 当前上下文存入 PCB，加载下一个进程的 PCB
- `__dummy`: 切用户栈，sret 返回用户段，而 sepc 是我们初始化的时候就指定的的 USER_START
- `ENTRY`: PC跳转至ENTRY，但是此时该页的映射并未完成，PAGE FAULT
- `_traps`: PAGE FAULT，保存上下文进入trap_handler
- `trap_handler`: 确认是PAGE FAULT后，调用do_page_fault
- `do_page_fault`: 根据current的vma确认是段错误、文件页缺页还是匿名页缺页，分配新页，填写内容，填写页表，返回
- `_traps`: 恢复上下文返回，此后对应页已有映射
- `ENTRY`: 恢复执行，直到调用fork
- `_traps`: 保存上下文，进入trap_handler
- `trap_handler`: 确认是fork后，调用sys_clone
- `sys_clone`: 进行一定的拷贝以初始化子进程，初始化完成后加入调度队列
    -  将父进程kernel stack 所在页拷贝一份给子进程，其中包括
          - task_struct: 位于该页低地址，其中内容在__switch_to到至子进程的时候会被加载，以下项需要改动
              - pid: 子进程的新pid
              - thread.sp: 换到子进程后系统栈的起始地址，注意切换过来时栈内已有数据
              - thread.ra: __switch_to到子进程后，__switch_to函数结束，应该ret到子进程的__return_from_fork
              - thread.sscratch: 子进程在内核态的sscratch，在返回用户态时会与sp交换，所以实质是子进程用户态的sp (1)
              - satp: 根据子进程页表修改
              - pgd: 子进程页表
          - pt_regs: 位于该页高地址，其中内容在子进程从内核态返回用户态时将会被加载，以下项需要改动  
              - a0: 返回用户态后携带的调用返回值，也就是子进程得到的fork返回值，0
              - sepc: fork对应ecall的下一条指令
- `_traps`: 父进程fork完毕，携带子进程pid恢复用户态上下文返回
- `fork`: 回到用户态，继续执行父进程直到被调度走,随后调度算法选择子进程
- `__switch_to`: 保存父进程上下文至父进程task_struct,从子进程task_struct中恢复子进程内核态上下文
- `__return_from_fork`: 子进程从pt_regs中恢复用户态上下文，包括返回值0，从trap返回ecall下一条指令，继续执行
```
</div>

1.  正常来说返回用户态的sp应该从pt_regs中恢复（文档中也是这么说的），但我实践上是从sscratch恢复的，这里应该根据具体实现修改。

## 调度算法

我们的task数组大小是`NR_TASKS`,所以我们要做到

- 只初始化指定数量的进程，而不是填满整个数组
- 调度的时候要遍历数组，但是只会调度那些有效的task

## 返回值异常

如果忘了将子进程返回用户态的地址设置为ecall下一条，可能导致fork返回值异常。设想如下情况：

- idle进程pid为0，父进程为1，子进程为2
- 调度子进程后sepc指向ecall，所以子进程返回用户态后继续执行ecall
- 子进程执行ecall再次进行fork，fork出新的子进程，在此次fork中，父进程为2，子进程为3
- 2进程完成fork返回，此时返回的是ecall的下一条（因为系统调用中会将sepc+4），返回值为3

可以看到2进程因为额外进行了一次fork所以返回值不再是其作为1的子进程拿到的0，而是作为3的父进程拿到的3，这就发生了错误