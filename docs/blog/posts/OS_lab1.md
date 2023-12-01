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

# 操作系统 - lab1 时钟中断

!!! abstract
    一个 kernel 的运行流程总结

<!-- more -->

!!! info "基本信息"
    时间：2023 秋冬

    实验文档：[:octicons-book-16:](https://zju-sec.github.io/os23fall-stu/lab1/)

# kernel 执行流程

<div class="annotate" markdown>
- `opensbi`执行完毕
- `_start`: 完成 stvec， sie， mtimecmp， sstatus 和栈的设置
- `start_kernel`: 进行一些输出，进入 test()死循环，直到时钟中断
- `_traps`: 时钟中断，保存好上下文后调用中断处理程序 trap_handler
- `trap_handler`: 确认是时钟中断后调用 clock_set_next
- `clock_set_next`: 利用 sbi_ecall 设置下一次中断时间
- `_traps`: 返回_traps 后恢复上下文 sret 返回死循环
- `test`: 死循环直到时钟中断，重复上述流程
</div>

$\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad$