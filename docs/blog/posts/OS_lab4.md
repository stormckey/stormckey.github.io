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
    比较 high level 的讲一下一些思想和需要注意的地方，很多细节问题还是要自己决定和思考的哒
<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-sec.github.io/os23fall-stu/lab4/)

## CPU 执行流程

<div class="annotate" markdown>
- opensbi 执行完毕
- _start: 完成 stvec, sie, mtimecmp, sstatus(1) 和栈的设置, 然后依次调用以下函数
    - setup_vm: 填写页表
    - relocate: 用设置好的页表修改 satp, 启动虚拟内存
    - mm_init: 完成内存分配函数的初始化
    - setup_vm_final: 切换到新的页表
    - task_init: 初始化进程
        - 对于idle以外的线程,需要在task_struct中额外给定以下信息:
            - sepc: 此线程被调度后从S Mode 回 U Mode的地址,显然就是用户程序起始地址 USER_START
            - sscratch: 用户栈顶,约定为USER_END
            - sstatus: 进行设置使得sret后我们回到 U Mode 而非 S Mode
            - satp: 每个进程都有自己的物理地址空间和虚拟地址空间,彼此隔离
                - 我们希望各进程间隔离,这就需要每个进程各自有一份二进制的文件的拷贝(2) 
                - 分配新页拷贝二进制文件后(3),把这些页的物理地址映射到USER_START开头的虚拟地址
                - 分配新的一页作栈,把这一页的物理地址映射到USER_END-4K
                - 写入satp
- start_kernel: 不进入test等时钟中断(4),而是直接调用schedule调度走
- switch_to: 在调度中选择下一个要调度的线程
- __switch_to: 当前上下文存入PCB,加载下一个进程的PCB(7)
- __dummy: 切换用户栈,sret返回用户段(5),而sepc是我们初始化的时候制定的USER_START(6)
- USER_START: 开始执行用户态代码,包括各种系统调用,直到时间片用完
- _traps: 时钟中断,保存上下文,调度下一个进程
- __switch_to: 同上,此后轮流调度
</div>

1.  注意对sstatus的设置禁止中断,这意味着我们的idle进程不会被时钟中断调度走
2.  二进制文件里有代码和数据等,对于那些全局变量我们当然希望各进程隔离.方便起见我们全都拷贝
3.  注意我们的映射是在页之间的,比如0x00010000起的虚拟页映射到0x80000000起的页,如果我们的程序入口在0x100e8,那么我们的第一行代码应该拷贝至0x800000e8而不是0x80000000
4.  因为时钟中断之前已经ban掉了
5.  回用户段后中断才重新enable, 因为我们直接设置好了sstatus的SPIE
6.  sepc在__switch_to中就已经load好了
7.  这里加载的PCB就是我们task_init的时候写好的,注意这里加载的ra我们初始化时设置为__dummy

## 注意事项

### uapp的加载

在vmlinux.lds中,我们指定了uapp.S文件会被加载到 _sramdisk,_eramdisk之间

- 如果uapp.S中我们用的是纯二进制文件,那么_sramdisk第一行就是程序第一行
- 如果uapp.S中我们用的是elf文件,我们需要解码elf头来定位具体的文件位置

## phdr->p_flags

注意这一项虽然是声明权限的的但定义不等同于页表项的perm,定义如下:

![](images/OS_lab4/2023-12-01-17-51-47.png#pic)
