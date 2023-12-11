---
comments: true
authors:
    - stormckey
categories:
    - Lab
    - OS
date: 2023-12-01
nostatistics: true
---
# 操作系统 - lab4 用户态
!!! abstract
    一些踩过的坑，以及一个 kernel 执行流程
<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-sec.github.io/os23fall-stu/lab4/)

## kernel 执行流程

<div class="annotate" markdown>
```title="kernel 执行流程" hl_lines="7-17 20-22" linenums="0"
- `opensbi` 执行完毕
- `_start`: 完成 stvec， sie， mtimecmp， sstatus(1) 和栈的设置，然后依次调用以下函数
    - `setup_vm`: 填写页表
    - `relocate`: 用设置好的页表修改 satp， 启动虚拟内存
    - `mm_init`: 完成内存分配函数的初始化
    - `setup_vm_final`: 切换到新的页表
    - `task_init`: 初始化进程
        - 对于 idle 以外的线程，需要在 task_struct 中额外给定以下信息：
            - `sepc`: 此线程被调度后从 S Mode 回 U Mode 的地址，显然就是用户程序起始地址 USER_START
            - `sscratch`: 用户栈顶，约定为 USER_END
            - `sstatus`: 进行设置使得 sret 后我们回到 U Mode 而非 S Mode
            - `satp`: 每个进程都有自己的物理地址空间和虚拟地址空间，彼此隔离
                - 我们希望各进程间隔离，这就需要每个进程各自有一份二进制的文件的拷贝(2)
                - 分配新页拷贝二进制文件后，新建页表,把这些页的物理地址映射到 USER_START 开头的虚拟地址
                - 分配新的一页作栈，把这一页的物理地址映射到 USER_END-4K
                - 根据新页表地址计算satp
- `start_kernel`: 不进入 test 等时钟中断(3)，而是直接调用 schedule 调度走
- `schedule`: 根据policy选择下一个要调度的线程,调用 switch_to 至该线程
- `switch_to`: 获取先后线程的PCB地址，调用__switch_to
- `__switch_to`: 当前上下文存入 PCB，加载下一个进程的 PCB(6)
- `__dummy`: 切用户栈，sret 返回用户段(4)，而 sepc 是我们初始化的时候就指定的的 USER_START(5)
- `USER_START`: 开始执行用户态代码，包括各种系统调用，直到时间片用完
- `_traps`: 时钟中断，切系统栈，保存上下文，调度下一个进程
- `__switch_to`: 同上，此后轮流调度
```
</div>

1.  注意对 sstatus 的设置禁止中断，这意味着我们的 idle 进程不会被时钟中断调度走
2.  二进制文件里有代码和数据等，对于那些全局变量我们当然希望各进程隔离.方便起见我们全都拷贝
3.  因为时钟中断之前已经 ban 掉了
4.  回用户段后中断才重新使能，因为我们直接设置好了 sstatus 的 SPIE
5.  sepc 在__switch_to 中就已经 load 好了
6.  这里加载的 PCB 就是我们 task_init 的时候写好的，注意这里加载的 ra 我们初始化时设置为__dummy

## uapp 的加载

在 vmlinux.lds 中，我们指定的 uapp.S 文件会被加载到 _sramdisk，_eramdisk 之间

- 如果 uapp.S 中我们用的是纯二进制文件，那么_sramdisk 第一行就是程序第一行
- 如果 uapp.S 中我们用的是 elf 文件，我们需要解码 elf 头来定位具体的二进制位置， 同时elf中也制定了程序入口一类的信息

## phdr->p_flags

注意这一项虽然是声明权限的的但定义不等同于页表项的 perm，定义如下：

![](images/OS_lab4/2023-12-01-17-51-47.png#pic)

## 执行权限

注意设置好页表和 sstatus 保证运行用户态代码时权限检查能够通过，否则会导致 scause = 0xc 的 inst page fault 此时也许我们可以在 gdb 中读信息但是一执行就出错

## 拷贝问题

虚拟内存映射是以页为单位的，比如 0x00010000 起的虚拟页映射到 0x80000000 起的物理页，如果我们的程序入口在 0x100e8，那么我们应该把这个入口拷贝至 0x800000e8 而不是 0x80000000

## 栈切换

在_traps 中，对于一些内核线程发起的异常是不需要切换栈的，我们通过检查 sscratch 为 0 来确认这一点

这一检查需要用到额外的寄存器（如 t0），但是我们是要保证 t0 的值在中断前后值不变，所以不能直接用，需要先压栈，返回之前记得恢复

!!! bug
    这里提到的压栈的办法在此处仍然可行，但在Lab5中会遇到问题，现在有一个更好用也更简洁的[:octicons-link-16:方法](https://stormckey.github.io/blog/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F---lab5-demand-paging/#_1)
