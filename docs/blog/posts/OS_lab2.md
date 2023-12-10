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

# 操作系统 - lab2 线程调度

!!! abstract
    一些踩过的坑，以及一个 kernel 的运行流程总结

<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-sec.github.io/os23fall-stu/lab2/)

## kernel 执行流程

<div class="annotate" markdown>
```title="kernel 执行流程" hl_lines="4-9 11-18" linenums="0"
- `opensbi`执行完毕
- `_start`: 完成 stvec， sie， mtimecmp， sstatus 和栈的设置，然后依次调用以下函数
    - `mm_init`: 完成内存分配函数的初始化
    - `task_init`: 完成对所有线程的 PCB 的初始化(1)，包括当前正在运行的 idle 线程
        - `test_init`: 该函数调用会填好 task_test_counter 和 1task_test_priority 两个数组用于给我们后续初始化使用
        - 分配新页作为 idle 的 PCB，填写并且设置为 current
        - 迭代为每个线程分配并填写 PCB，注意其中 ra 和 sp 的设置
            - ra: ra 固定为__dummy，这是我们为线程被调度后设置的返回地址
            - sp: 直接用分配给 PCB 的这一页做栈，栈顶自然就是 PCB 地址+4K
- `start_kernel`: 进入 test()死循环，直到时钟中断
- `_traps`: 时钟中断，保存好上下文后调用中断处理程序 trap_handler
- `trap_handler`: 确认是时钟中断后，设置下次中断时间，进入 do_timer()检查该线程剩余时间
- `do_timer`: 如果是 idle 或者时间用尽直接调用 schedule()调度走，否则时间减一
- `schedule`: 根据 policy 选择下一个要调度的线程，调用 switch_to()至该线程(2)，如果所有线程时间都用完了就先初始化时间再选择
- `switch_to`: 前后线程的 PCB，调用__switch_to
- `__switch_to`: 保存上下文，加载下一个线程的 PCB(3)
- `__dummy`: 从__switch_to 返回，返回地址就是 PCB 中恢复的__dummy.我们在 dummy 中结束此次中断用 sret 回到该线程执行的函数 dummy
- `dummy`: 该线程主函数，切换回来后进行一次输出然后循环等待时钟中断
- `_traps`: 时钟中断，一般是剩余时间减一然后继续，直到时间用完，再次进入 schedule 循环
```
</div>

1.  也就是帮每个线程填好 task_struct
2.  对于这个被调度走的线程来说，他只是调用了 switch_to 函数，然后等着再返回罢了.虽然实际上 CPU 把此线程踢开去干别的活了，但本线程并不知道.所以 CPU 再次调度回此线程的时候，就该从 switch_to 函数返回，从而让该线程无感衔接.
3.  加载后我们的 sp 会设为之前分配页的顶端，ra 会设置为__dummy，这都是初始化时设计的


## 注意事项

注意到我们对于非 idle 线程第一次从 __switch_to 返回的都是 __dummy， 这是我们初始化的 PCB 被恢复出来的 ra 决定的

但是该线程第二次被调度的时候，它恢复的 PCB 就是它之前自己存下来的而不再是初始化的.这个存下来的 ra 就是 switch_to，__switch_to 函数运行时的 ra 当然是__switch_to 的调用者
