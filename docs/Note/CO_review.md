# 计组拾遗
!!! warning "极其简略，只有部分易忘、或不显然的知识点"

!!! info "整理自[:octicons-link-16:咸鱼暄的代码空间](https://xuan-insr.github.io/computer_organization/1_prelude/)"

!!! tip "[:octicons-link-16:这里](https://bank.engzenon.com/tmp/60746e35-6aec-4163-86ed-7fdec0feb99b/626db954-7f2c-45af-9aa3-42dfc0feb99b/Computer_Organization_Manual_solution.pdf)是答案"
## Ch2 Instructions

- PC relative addressing: `PC + offset` 而非 `PC + 4 + offset`
- I 类型有两种，分别是：
  ![](images/CO_review/2023-03-30-21-57-02.png#pic)
  一般都是第一类，第二类是因为立即数移位指令不需要那么多位
- SB 和 UJ类型都不存最低位，因为他们的目的地是指令（word alignment），一般最后两位都是0（因为存在16位的指令所以不绝对）
- 合理利用`bgeu`来检测越界（小于零或者大于某个数）
- `lui`加载了立即数的高20位后，用`aadi`加载低12位，若因符号扩展导致进位，只要多加1000就可以抵消FFFFF000的影响

还有几张常用表：
![](images/CO_review/2023-03-31-17-29-23.png#pic)

![](images/CO_review/2023-03-31-17-29-33.png#pic)

![](images/CO_review/2023-03-31-17-29-45.png#pic)

（下图里的j imm要改成PC+imm）
![](images/CO_review/2023-03-31-17-30-14.png#pic)
## Ch3 Arithmetic

- 检测加法溢出:最高运算单元的Cin Cout进行异或，不一样就是溢出
- 最高位牵出一根线到最低位，与其他所有位都是0就可以组成slt的输出信号了
- IEEE 754 注意两点 一是1+8+23 = 32 ｜1 + 11 + 52 = 64；二是下溢的非规格数的exponent跟规格数的最小exponent是一样的，这样设计就可以让 0.1111111...（下溢最大） -> 1.0000000（规格最小）...连续
- 浮点加法：注意对齐改变的是小的指数那个
- 浮点乘法，注意减去bias

